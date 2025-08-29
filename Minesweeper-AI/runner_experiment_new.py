from minesweeper_new import Minesweeper, MinesweeperAI
import time

HEIGHT = 8
WIDTH = 8
MINES = 8

def run_experiment(num_games=1000, height=8, width=8, mines=8):
    """
    Chạy thực nghiệm tự động cho agent AI.
    """
    wins = 0
    losses = 0

    print(f"Starting experiment with {num_games} games (Board {height}x{width}, {mines} mines)...")

    start_time = time.time()

    for i in range(num_games):
        game = Minesweeper(height=height, width=width, mines=mines)
        ai = MinesweeperAI(height=height, width=width)

        flags = set()

        while True:
            if game.mines == flags:
                wins += 1
                break

            move = ai.decide_move()

            """
                Xử lý khi không còn nước đi nào
                Nếu AI trả về None, tức là nó không thể đi được nữa.
                Vì đã kiểm tra thắng ở trên, nên nếu tới đây, ta tính là thua.
            """
            if move is None:
                losses += 1
                break

            """
                Xử lý nước đi
                Nếu đi vào mìn -> thua
            """
            if game.is_mine(move):
                losses += 1
                break
            else:
                nearby = game.nearby_mines(move)
                ai.add_knowledge(move, nearby)
                flags = ai.getFlags()

    end_time = time.time()
    total_time = end_time - start_time

    print("\nExperiment completed.")
    print(f"Number of games: {num_games}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    win_rate = (wins / num_games) * 100
    print(f"Win rate: {win_rate:.2f}%")
    print(f"Total time: {total_time:.2f} giây")

    return wins, losses, win_rate


if __name__ == "__main__":
    run_experiment(num_games=1000, height=HEIGHT, width=WIDTH, mines=MINES)