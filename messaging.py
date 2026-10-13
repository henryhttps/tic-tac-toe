HEADER_BYTES = 8

FLAG_X_MOVE = 1 << 13
FLAG_O_MOVE = 1 << 12
FLAG_X_WIN = 1 << 11
FLAG_O_WIN = 1 << 10
FLAG_TIE = 1 << 9
FLAG_ERROR = 1 << 8

EMPTY, X, O = 0, 1, 2


def encode_message(game_id, message_id, flags, game_state, message):
    header = ((game_id & 0xFFFFFF) << 40) | ((message_id & 0xFF) << 32) \
        | ((flags & 0x3FFF) << 18) | (game_state & 0x3FFFF)
    return header.to_bytes(HEADER_BYTES, byteorder='big') + message.encode('utf-8')


def decode_message(message):
    if len(message) < HEADER_BYTES:
        raise ValueError("message too short")
    header = int.from_bytes(message[:HEADER_BYTES], byteorder='big')
    game_id = (header >> 40) & 0xFFFFFF
    message_id = (header >> 32) & 0xFF
    flags = (header >> 18) & 0x3FFF
    game_state = header & 0x3FFFF
    text = message[HEADER_BYTES:].decode('utf-8', errors='replace')
    return game_id, message_id, flags, game_state, text


def encode_game_state(game_state):
    bits = 0
    for square in game_state:
        bits = (bits << 2) | (square & 0b11)
    return bits


def decode_game_state(game_bits):
    return [(game_bits >> (2 * (8 - i))) & 0b11 for i in range(9)]
