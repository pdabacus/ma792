"""
read in imdb reviews and preprocess by removing symbols and stopwords
"""

import torch
import torch.nn
import numpy as np

import glove
import imdb

_version = "1.0.0"

class HappyAngryRNN(torch.nn.Module):

    def __init__(self, review_len, glove_embedding, lstm_hidden, lstm_layers, lstm_dropout, output_dim):
        super().__init__()

        self.review_len = review_len
        self.glove = glove_embedding
        self.lstm_hidden = lstm_hidden
        self.lstm_layers = lstm_layers
        self.output_dim = output_dim

        #embedding layer
        self.embedding = torch.nn.Embedding.from_pretrained(
            torch.from_numpy(np.matrix(glove_embedding._vectors)),
            freeze=True,
            padding_idx=0,
        )

        #lstm layer
        self.lstm = torch.nn.LSTM(
            self.embedding.embedding_dim,
            lstm_hidden,
            num_layers=lstm_layers,
            bidirectional=True,
            dropout=lstm_dropout,
            batch_first=True
        )

        #dense layer
        self.fc = torch.nn.Linear(lstm_hidden * 2, output_dim)

        #activation function
        self.sig = torch.nn.Sigmoid()

    def forward(self, text):
        #text = [batch_size, review_len]

        embedded = self.embedding(text)
        #embedded = [batch_size, review_len, glove_embed_dim]

        output, (hidden, cell) = self.lstm(embedded)
        #hidden = [num_layers * num_directions, batch_size, hidden_dim]
        #cell = [num_layers * num_directions, batch_size, hidden_dim]

        # concat the final forward and backward hidden state
        hidden_ends = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        #hidden_ends = [batch_size, hidden_dim * num_directions]

        dense_outputs = self.fc(hidden_ends)
        #dense_outputs = [batch_size, 2]

        outputs = self.sig(dense_outputs)
        #outputs = [batch_size, 2]

        return outputs

    def predict(self, sentence):
        tokenized = imdb.IMDB.process(sentence)
        encoded = self.glove.encode(tokenized, self.review_len)
        pred = self(torch.from_numpy(np.matrix(encoded))).squeeze().tolist()
        return {"positive": pred[0], "negative": pred[1]}


hyperparams = {
    "review_length": 600,
    "test_percent": 0.10,
    "batch_size": 50,
    "lstm_hiddin_dim": 32,
    "lstm_layers": 2,
    "lstm_dropout": 0.2
}

def main():
    output_dim = 2
    model = HappyAngryRNN(
        hyperparams["review_length"],
        glove.GloVe("glove/glove.6B.100d.txt"),
        hyperparams["lstm_hiddin_dim"],
        hyperparams["lstm_layers"],
        hyperparams["lstm_dropout"],
        output_dim
    )

    #torch.save(model.state_dict(), "happy_angry_rnn.pt")
    model.load_state_dict(torch.load("happy_angry_rnn.pt"))
    model.eval()

    s = "this song is very good i would listen again"
    print(s)
    print(model.predict(s))

if __name__ == "__main__":
    main()
