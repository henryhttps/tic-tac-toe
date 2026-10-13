import random
import socket
import sys

from messaging import *

SYMBOLS = {EMPTY: ' ', X: 'X', O: 'O'}
LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]


def print_board(board):
    rows = []
    for r in range(3):
        rows.append(' ' + ' | '.join(SYMBOLS[board[r*3 + c]] for c in range(3)))
    print('\n' + '\n---+---+---\n'.join(rows) + '\n')
    print('Squares are numbered 1-9, left to right, top to bottom.')


def send_receive(sock, addr, data, game_id):
    timeout = 1
    for _ in range(4):
        sock.settimeout(timeout)
        sock.sendto(data, addr)
        try:
            while True:
                reply, _ = sock.recvfrom(2048)
                try:
                    fields = decode_message(reply)
                except ValueError:
                    continue
                if fields[0] == game_id:
                    return fields
        except socket.timeout:
            timeout *= 2
    print("Error: no response from server after 4 attempts.")
    sys.exit(1)


def get_move(board):
    while True:
        raw = input("Your move (1-9): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= 9 and board[int(raw) - 1] == EMPTY:
            return int(raw) - 1
        print("Invalid move: choose an empty square numbered 1-9.")


def play(sock, addr, name):
    game_id = random.randint(0, 0xFFFFFF)
    game_id, msg_id, flags, state, text = send_receive(
        sock, addr, encode_message(game_id, 0, 0, 0, name), game_id)

    while True:
        if text:
            print("Server:", text)
        board = decode_game_state(state)
        print_board(board)

        if flags & FLAG_ERROR:
            print("Server reported an error; exiting.")
            sys.exit(1)
        if flags & FLAG_X_WIN:
            print("X wins!"); return
        if flags & FLAG_O_WIN:
            print("O wins!"); return
        if flags & FLAG_TIE:
            print("It's a tie!"); return

        me = X if flags & FLAG_X_MOVE else O
        board[get_move(board)] = me
        msg_id = (msg_id + 1) & 0xFF
        data = encode_message(game_id, msg_id, 0, encode_game_state(board), "")
        game_id, msg_id, flags, state, text = send_receive(sock, addr, data, game_id)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <host> <port>")
        sys.exit(1)
    addr = (sys.argv[1], int(sys.argv[2]))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    name = input("Enter your name: ")
    while True:
        play(sock, addr, name)
        if input("Play again? (y/n): ").strip().lower() != 'y':
            break


if __name__ == '__main__':
    main()
