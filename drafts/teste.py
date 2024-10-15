from core.encoding import encoder, decoder

def teste(message):
    encoded_message = encoder(message)
    decoded_message = decoder(encoded_message)
    print(decoded_message)

teste(['oi meu chapa', 'fica frio ai'])