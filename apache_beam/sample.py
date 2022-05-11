import re

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

# 読み込み先のファイル
input_file = "./input/data.txt"
# 出力先のファイル
ouput_file = "./output/export.txt"

# pipline objectの作成
pipline_options = PipelineOptions()

with beam.Pipeline(options=pipline_options) as p:

    # テキストの読み込み処理
    lines = p | ReadFromText(input_file)

    # 各単語の頻度を数える
    # 処理の流れ　データの分割>文字一つ一つをカウント>同じ文字について足し合わせる
    counts = (
        lines
        | 'Split' >> beam.FlatMap(lambda x: re.findall(r'[A-Za-z\']+', x))
        | 'PairWithOne' >> beam.Map(lambda x: (x, 1))
        | 'GroupAndSum' >> beam.CombinePerKey(sum))

    # フォーマット修正処理
    def format_result(word_count):
        (word, count) = word_count
        return "{}:{}".format(word, count)
    # 結果のフォーマットを調整
    output = counts | 'Format' >> beam.Map(format_result)

    # ファイルとして結果を出力する
    output | WriteToText(ouput_file)
