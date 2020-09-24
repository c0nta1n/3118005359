import jieba
import re
import gensim
import sys


def sentenceclean(path):
    str = ''
    f = open(path, 'r', encoding='UTF-8')
    '''读第一句'''
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    '''jieba中文分词'''
    sentence1 = jieba.lcut(str)
    '''由于是中文文本的查重，把除中文外的符号全部清除'''
    d = "[\u4e00-\u9fa5]+"
    sentence2 = []
    for i in sentence1:
        a = re.findall(d, i)
        sentence2 += a
    f.close()
    return sentence2


def calc_similarity(str1, str2):
    texts = [str1, str2]
    '''建立字典'''
    dictionary = gensim.corpora.Dictionary(texts)
    '''使用doc2bow制作语料库.
    语料库是一组向量，向量中的元素是一个二元组（编号、频次数），对应分词后的文档中的每一个词。'''
    corpus = [dictionary.doc2bow(text) for text in texts]
    '''similarities.MatrixSimilarity类仅仅适合能将所有的向量都在内存中的情况。
       例如，如果一个百万文档级的语料库使用该类，可能需要2G内存与256维LSI空间。 
       如果没有足够的内存，你可以使用similarities.Similarity类。
       该类的操作只需要固定大小的内存，因为他将索引切分为多个文件（称为碎片）存储到硬盘上了。
       它实际上使用了similarities.MatrixSimilarity和similarities.SparseMatrixSimilarity两个类。
       因此它也是比较快的，虽然看起来更加复杂了。
       similarity用于计算相似度，返回的是一组列表'''
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    '''计算text1的向量'''
    test_corpus_1 = dictionary.doc2bow(str1)
    '''计算测试文档的相似度'''
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim


def main():
    if __name__ == '__main__':
        path1 = "F:\python\project\orig.txt"
        path2 = "F:\python\project\orig_0.8_del.txt"
        save_path = "F:\python\project\save.txt"
        str1 = sentenceclean(path1)
        str2 = sentenceclean(path2)
        similarity = calc_similarity(str1, str2)
        print("文章相似度： %.4f" % similarity)
        f = open(save_path, 'w', encoding="utf-8")
        f.write("文章相似度： %.4f" % similarity)
        f.close()
        print('参数个数为:', len(sys.argv), '个参数。')
        print('参数列表:', str(sys.argv))
        print('脚本名为：', sys.argv[0])
        for i in range(1, len(sys.argv)):
            print('参数 %s 为：%s' % (i, sys.argv[i]))


if __name__ == '__main__':
    main()
