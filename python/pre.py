#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created by Chihiro Miyamoto (2017)
#
# データの前処理
# ・移動平均による平滑化
#
# 環境
# ・Python 3.6
# 必要
# ・numpyのインストール
#

import glob
import numpy

# ファイルの3行無視処理
# input：生データが入ってるディレクトリまでのパス/ファイルの正規表現
# output：# data/pre/に生データの文頭3行無視版
def file_rw(input_path):
    for file in glob.glob(input_path):
        print('Reading ' + file) # ファイル名表示
        # 出力先パスの設定
        input_split = file.split("/")
        output_path = input_split[0] + "/data/pre/" + input_split[3]
        print('Outputing ' + output_path)

        i = 0   # 1行目判断フラグ
        for line in open(file, 'r'):
            if(i < 3):  # 3行無視
                i += 1  # フラグ更新
            else:
                # print(line, end="")
                if(i == 3): # 1行目書き込み
                    f = open(output_path, "w")  # w：書込モード
                    i += 1  # フラグ更新
                    print(line, end="", file=f)
                else:       # 2行目以降の追記
                    f = open(output_path, "a")  # a：追記モード
                    print(line, end="", file=f)


# 移動平均したデータファイルの出力
# input：生データが入ってるディレクトリまでのパス/ファイルの正規表現
# output：# data/pre/に生データの文頭3行無視版
def file_rw2(input_path):
    for file in glob.glob(input_path):
        print('Reading ' + file) # ファイル名表示
        i = 0   # 1行目判断フラグ
        for line in open(file, 'r'):
            # print(line, end="")
            data_split = line.split("	")
            if(i == 0):
                x = numpy.array(float(data_split[0]))   # float型に変換
                y = numpy.array(float(data_split[1].rstrip("\n")))  # float型変換+改行コード削除
                i += 1  # フラグ更新
            else:
                x = numpy.append(x, float(data_split[0]))
                y = numpy.append(y, float(data_split[1].rstrip("\n")))

        # 移動平均した配列の取得
        x = moving_average(x, 5)
        y = moving_average(y, 5)

        # 出力先パスの設定
        input_split = file.split("/")
        output_path = input_split[0] + "/data/ma/" + input_split[3]
        print('Outputing ' + output_path)

        # ファイルの出力処理
        for j in range(x.size):
            out_data = str(x[j]) + u'	' + str(y[j])
            if(i == 0): # 1行目書き込み
                f = open(output_path, "w")
                i += 1
                print(out_data, end="\n", file=f)
            else:       # 2行目以降の追記
                f = open(output_path, "a")
                print(out_data, end="\n", file=f)


# k-移動平均フィルタ
# input x：floatのデータ群
# input k：窓サイズ
# output x_ave：入力されたデータ群のk平均のデータ群
def moving_average(x, k):
    k_window = numpy.ones(k)/k
    x_ave = numpy.convolve(x,k_window,'valid')    # 先頭と末尾の平均を取れない部分を省略
    return x_ave

# メイン関数
if __name__ == "__main__":
    # file_rw("../data/raw/*")    # 1回だけでよし
    file_rw2("../data/pre/*")
