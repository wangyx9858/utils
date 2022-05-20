import pandas as pd
from tabulate import tabulate

# 买入一手筹码的钱
BUY_IN = 50

# 姓名：输赢手数
input_data = dict(
    张三=3,
    李四=9,
    王五=-11,
)
input_data = dict(sorted(input_data.items(), key=lambda item: item[1], reverse=True))

# 水费：饮料、晚饭、场地费等等。
water_money = 214


def main():
    all_win = sum([i for i in input_data.values() if i > 0])
    all_lose = sum([i for i in input_data.values() if i < 0])
    balance_money = int((all_win + all_lose) * BUY_IN)
    datas = []
    for name, desktop_win_hand in input_data.items():
        win_ratio = desktop_win_hand / all_win
        lose_ratio = desktop_win_hand / all_lose
        desktop_win = int(desktop_win_hand * BUY_IN)
        # 平摊水费，只有赢的人平摊
        split_water_money = -int(win_ratio * water_money) if desktop_win_hand > 0 else 0

        # 少的钱从赢的人身上扣。多的钱分给输的人。目的是保护输的人。
        if balance_money > 0:
            split_balance_money = -int(abs(win_ratio * balance_money)) if desktop_win_hand > 0 else 0
        elif balance_money < 0:
            split_balance_money = int(abs(lose_ratio * balance_money)) if desktop_win_hand < 0 else 0
        else:
            split_balance_money = 0
        final_win = desktop_win + split_balance_money + split_water_money
        data = [name, desktop_win, split_balance_money, split_water_money, final_win]
        datas.append(data)

    df = pd.DataFrame(datas, columns=['姓名', '桌面盈利', '桌面平摊', '平摊水费', '最终盈利'])
    df.index += 1
    ret = tabulate(df, headers='keys', tablefmt='psql')
    print(ret)


if __name__ == '__main__':
    main()
