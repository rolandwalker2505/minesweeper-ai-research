import random
import time
import statistics

from minesweeper_new import Minesweeper, MinesweeperAI as MinesweeperAIHybrid
from old.minesweeper import MinesweeperAI as MinesweeperAIBase

def play_one_game(ai_class, height, width, mines):
    game = Minesweeper(height=height, width=width, mines=mines)
    ai = ai_class(height=height, width=width)

    if ai_class is MinesweeperAIBase:
        def base_decide_move():
            move = ai.make_safe_move()
            if move:
                return move
            return ai.make_random_move()

        ai.decide_move = base_decide_move

    while True:
        # Agent cơ sở không có getFlags, nên ta truy cập trực tiếp
        flags = ai.getFlags()
        if game.mines == flags:
            return "win"

        move = ai.decide_move()

        if move is None:
            final_flags = ai.getFlags()
            if game.mines == final_flags:
                return "win"
            return "loss"

        if game.is_mine(move):
            return "loss"
        else:
            ai.add_knowledge(move, game.nearby_mines(move))


def run_one_paired_trial(trial_num, num_games, height, width, mines):
    wins_base = 0
    wins_hybrid = 0

    start_time_base = time.time()
    for i in range(num_games):
        # seed = f"trial_{trial_num}_game_{i}"
        # random.seed(seed)
        random_seed = random.randint(0, 9999)
        random.seed(random_seed)
        if play_one_game(MinesweeperAIBase, height, width, mines) == "win":
            wins_base += 1

    end_time_base = time.time()
    time_base = end_time_base - start_time_base

    start_time_hybrid = time.time()
    for i in range(num_games):
        # seed = f"trial_{trial_num}_game_{i}"
        # random.seed(seed)
        random_seed = random.randint(0, 9999)
        random.seed(random_seed)
        if play_one_game(MinesweeperAIHybrid, height, width, mines) == "win":
            wins_hybrid += 1
    end_time_hybrid = time.time()
    time_hybrid = end_time_hybrid - start_time_hybrid

    win_rate_base = (wins_base / num_games) * 100
    win_rate_hybrid = (wins_hybrid / num_games) * 100
    print(
        f"Lượt {trial_num} hoàn tất: "
        f"Cơ sở: {wins_base}/{num_games} ({win_rate_base:.2f}%) - "
        f"Cải tiến: {wins_hybrid}/{num_games} ({win_rate_hybrid:.2f}%)"
    )
    return wins_base, wins_hybrid, time_base, time_hybrid


if __name__ == "__main__":
    NUM_TRIALS = 5
    NUM_GAMES_PER_TRIAL = 1000
    HEIGHT, WIDTH, MINES = 8, 8, 8

    base_results = []
    hybrid_results = []
    base_times = []
    hybrid_times = []

    start_time = time.time()

    for i in range(1, NUM_TRIALS + 1):
        wins_base, wins_hybrid, time_base, time_hybrid = run_one_paired_trial(
            trial_num=i,
            num_games=NUM_GAMES_PER_TRIAL,
            height=HEIGHT,
            width=WIDTH,
            mines=MINES
        )
        base_results.append(wins_base)
        hybrid_results.append(wins_hybrid)
        base_times.append(time_base)
        hybrid_times.append(time_hybrid)

    end_time = time.time()
    total_time = end_time - start_time

    base_mean = statistics.mean(base_results)
    hybrid_mean = statistics.mean(hybrid_results)
    base_stdev = statistics.stdev(base_results) if len(base_results) > 1 else 0
    hybrid_stdev = statistics.stdev(hybrid_results) if len(hybrid_results) > 1 else 0
    base_time_mean = statistics.mean(base_times)
    hybrid_time_mean = statistics.mean(hybrid_times)

    print("\n" + "=" * 50)
    print(" " * 10 + "KẾT QUẢ THỰC NGHIỆM TỔNG HỢP")
    print("=" * 50)
    print(f"Tổng số lượt chạy: {NUM_TRIALS}")
    print(f"Số ván mỗi lượt: {NUM_GAMES_PER_TRIAL}")
    print(f"Tổng thời gian: {total_time:.2f} giây")
    print("-" * 50)

    print("\n[ Agent Cơ sở (Logic CSP) ]")
    print(f"Số ván thắng mỗi lần: {base_results}")
    print(f"Thời gian chạy mỗi lần: {base_times}")
    print(f"Trung bình số ván thắng: {base_mean:.2f} / {NUM_GAMES_PER_TRIAL}")
    print(f"Tỷ lệ thắng trung bình: {(base_mean / NUM_GAMES_PER_TRIAL) * 100:.2f}%")
    print(f"Độ lệch chuẩn: {base_stdev:.2f}")
    print(f"Thời gian mỗi lần chạy trung bình: {base_time_mean:.2f}s")

    print("\n[ Agent Cải tiến (Hybrid) ]")
    print(f"Số ván thắng mỗi lần: {hybrid_results}")
    print(f"Thời gian chạy mỗi lần: {hybrid_times}")
    print(f"Trung bình số ván thắng: {hybrid_mean:.2f} / {NUM_GAMES_PER_TRIAL}")
    print(f"Tỷ lệ thắng trung bình: {(hybrid_mean / NUM_GAMES_PER_TRIAL) * 100:.2f}%")
    print(f"Độ lệch chuẩn: {hybrid_stdev:.2f}")
    print(f"Thời gian mỗi lần chạy trung bình (1000 ván): {hybrid_time_mean:.2f}s")
    print("=" * 50)