import numpy as np
import random
import matplotlib.pyplot as plt
import datetime

# 初期個体生成
def  create_genom(population):
#     乱数を２進数変換，ゼロ埋めしてマージ
    x =  [[random.randrange(0, 1024) for i in range(2)] for j in range(population)]
    x1 = [bin(x[i][0])[2:].zfill(10) for i in range(population)]
    x2 = [bin(x[i][1])[2:].zfill(10) for i in range(population)]
    chromosome = [[int(x1[i], 2), int(x2[i], 2)] for i in range(population)]
    return chromosome

# 2進数変換
def convert(chromosome, population):
#     １世代以降の２進数変換，マージ
    x1 = [chromosome[i][:int(len(chromosome[0]) / 2)] for i in range(len(chromosome))]
    x2 = [chromosome[i][int(len(chromosome[0]) / 2):] for i in range(len(chromosome))]
    chromosome = [[int(x1[i], 2), int(x2[i], 2)] for i in range(population)]
    return chromosome

# 評価
def evaluate(chromosome, population, n):
#     適合度をリストに格納し，リストを返す
    evaluated_data = list()
    for i in range(population):
        f = 0
        for j in range(n):
            f += (0.5 * np.sin(chromosome[i][j] * np.pi / 1024) * np.cos(20 * chromosome[i][j] * np.pi / 1024) + 0.5)
        evaluated_data.append(f / n)
    return  evaluated_data

# 選択
# selection_method == 0 : ルーレット選択
# selection_method == 1 : 期待値選択
def select(evaluated_data, population, selection_method):
    fitness_list = list()
    sum_fitness = sum(evaluated_data)
#     適合度を正規化するリスト
    fitness_list = [i / sum_fitness for i in evaluated_data]

#     ルーレット選択
    if selection_method == 0:
#         正規化した適合度の累積リストを作成，選択
        cumulate_list = list()
        cumulate_list = [0] * population
        selected_data = list()
        selected_data = [0] * len(fitness_list)

        for i in range(len(fitness_list)):
            if i == 0:
                cumulate_list[i] = fitness_list[i]
            else:
                cumulate_list[i] = fitness_list[i] + cumulate_list[i - 1]

        for i in range(population):
            a = random.uniform(0, 1.0)
            for j in range(len(cumulate_list)):
                if a <= cumulate_list[j]:
                    selected_data[i] = [j, evaluated_data[j]]
                    break
        return selected_data

#     期待値選択
    if selection_method == 1:
        selected_data = list()
#         期待値のリスト作成
        expected_value = [fitness_list[i] * population for i in range(len(fitness_list))]
#         再生数のリスト作成
        regen_list = [int(round(expected_value[i])) for i in range(len(fitness_list))]
#         設定個体数と再生数の差を取得
        diff = population - sum(regen_list)

#         設定個体数よりも再生数の総和が少なかった場合，最も適合度の高い期待値の再生数を増やす
        if sum(regen_list) < population:
            index_num = expected_value.index(max(expected_value))
            regen_list[index_num] += diff

#         設定個体数よりも再生数の総和が多かった場合，適合度の低い期待値の再生数から減らしていく
        if sum(regen_list) > population:
            tmp = list(expected_value)
            while diff != 0:
                hoge = min(tmp)
                index_num = expected_value.index(hoge)
                if regen_list[index_num] == 0:
                    tmp[index_num] = 100
                    continue
                regen_list[index_num] -= 1
                diff += 1

        for i in range(len(regen_list)):
            for j in range(regen_list[i]):
                selected_data.append([i, expected_value[i]])
        return selected_data

# 交叉
# crossover_method == 1 : 一点交叉
# crossover_method == 2 : 二点交叉
def crossover(selected_data, chromosome, population, crossover_method):
#     一点交叉
    if crossover_method == 0:
        selected_x1 = [bin(chromosome[selected_data[i][0]][0])[2:].zfill(10) for i in range(population)]
        selected_x2 = [bin(chromosome[selected_data[i][0]][1])[2:].zfill(10) for i in range(population)]
        selected_chrom = [selected_x1[i] + selected_x2[i] for i in range(population)]

        child = list()
#         個体数が偶数の場合
        if population % 2 == 0:
            for i in range(0, len(selected_chrom), 2):
                point1 = random.randrange(1, len(selected_chrom[0]))
                child_1 = selected_chrom[i][:point1] + selected_chrom[i + 1][point1:]
                child_2 = selected_chrom[i + 1][:point1] + selected_chrom[i][point1:]
                child.append(child_1)
                child.append(child_2)
#         個体数が奇数の場合
        else:
                for i in range(0, len(selected_chrom) - 1, 2):
                    point1 = random.randrange(1, len(selected_chrom[0]))
                    child_1 = selected_chrom[i][:point1] + selected_chrom[i + 1][point1:]
                    child_2 = selected_chrom[i + 1][:point1] + selected_chrom[i][point1:]
                    child.append(child_1)
                    child.append(child_2)
                child.append(selected_chrom[-1])

        return child

#     二点交叉
    if crossover_method == 1:
        selected_x1 = [bin(chromosome[selected_data[i][0]][0])[2:].zfill(10) for i in range(population)]
        selected_x2 = [bin(chromosome[selected_data[i][0]][1])[2:].zfill(10) for i in range(population)]
        selected_chrom = [selected_x1[i] + selected_x2[i] for i in range(population)]

        child = list()
#         個体数が偶数の場合
        if population % 2 == 0:
            for i in range(0, len(selected_chrom), 2):
                point1 = random.randrange(1, len(selected_chrom[0]) - 1)
                point2 = random.randrange(point1 + 1, len(selected_chrom[0]))
                child_1 = selected_chrom[i][:point1] + selected_chrom[i + 1][point1:point2] + selected_chrom[i][point2:]
                child_2 = selected_chrom[i + 1][:point1] + selected_chrom[i][point1:point2] + selected_chrom[i + 1][point2:]
                child.append(child_1)
                child.append(child_2)
#         個体数が奇数の場合
        else:
                for i in range(0, len(selected_chrom) - 1, 2):
                    point1 = random.randrange(1, len(selected_chrom[0]) - 1)
                    point2 = random.randrange(point1 + 1, len(selected_chrom[0]))
                    child_1 = selected_chrom[i][:point1] + selected_chrom[i + 1][point1:point2] + selected_chrom[i][point2:]
                    child_2 = selected_chrom[i + 1][:point1] + selected_chrom[i][point1:point2] + selected_chrom[i + 1][point2:]
                    child.append(child_1)
                    child.append(child_2)
                child.append(selected_chrom[-1])

        return child

# 突然変異
def mutate(child, mutation_p):
    for i in range(len(child)):
        tmp = list(child[i])
        for j in range(len(tmp)):
            if random.random() < mutation_p:
                tmp[j] = str(1 - int(tmp[j]))
        child[i] = ''.join(tmp)
    return child

if __name__ == '__main__':
#     設定
    population = 100
    n = 2
    mutation_p = 0.03
    max_generation = 1000
    generation = 0
    selection_method = 1
    crossover_method = 0
    selection = 'ルーレット選択' if selection_method == 0 else '期待値選択'
    cross = '一点交叉' if crossover_method == 0 else '二点交叉'


#     GAスタート
    file_name = str(selection_method) + str(crossover_method) + 'ga_{0:%Y_%m%d_%H%M_%S}'.format(datetime.datetime.now())
    f = open(file_name + '.txt', 'w')
    f.write('世代数 : 適合度(上位3要素)\n')
    plt_x = list()
    plt_y = list()
    while True:
        if generation >= max_generation:
            break
        else:
            if generation == 0:
                chromosome = create_genom(population)
            else:
                chromosome = convert(child, population)

            evaluated_data = evaluate(chromosome, population, n)

            display_list = list(evaluated_data)
            display_list.sort(reverse = True)
            plt_x.append(generation)
            plt_y.append(display_list[:1])
            f.write(str(generation) + '世代 : ' + str(display_list[:3]) + '\n')

            selected_data = select(evaluated_data, population, selection_method)
            child = crossover(selected_data, chromosome, population, crossover_method)
            child = mutate(child, mutation_p)

            generation += 1

    fig = plt.figure()
    plt.rcParams['font.family'] = 'IPAexGothic'
    plt.grid()
    plt.plot(plt_x, plt_y, label=selection + '\n' + cross)
    plt.legend()
    plt.legend(bbox_to_anchor=(1, 0), loc='lower right', borderaxespad=1, fontsize=12)
    plt.xlabel("世代数")
    plt.ylabel("適合度")
    plt.ylim(0.7, 1.02)
    plt.savefig(file_name + 'png')
    f.close()
