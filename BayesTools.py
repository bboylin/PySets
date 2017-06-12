# coding:utf-8
import tkFileDialog
import Tkinter
import csv


class BayesTools:
    def __init__(self):
        self.fileNameForTraining = '/'
        self.fileNameForTesting = '/'
        window = Tkinter.Tk()
        window.title("bayes")
        btnSelectTrainingSet = Tkinter.Button(
            window, text="选择训练集", command=self.selectTrainingSet)
        btnSelectTestingSet = Tkinter.Button(
            window, text="选择测试集", command=self.selectTestingSet)
        btnStart = Tkinter.Button(window, text="开始", command=self.start)
        btnSelectTrainingSet.pack()
        btnSelectTestingSet.pack()
        btnStart.pack()
        window.mainloop()

    def selectTrainingSet(self):
        self.fileNameForTraining = tkFileDialog.askopenfilename(initialdir='/')
        print self.fileNameForTraining

    def selectTestingSet(self):
        self.fileNameForTesting = tkFileDialog.askopenfilename(initialdir='/')
        print self.fileNameForTesting

    def start(self):
        attnum = 5  # attribute number
        attrname = ['content_similar', 'figure_url', 'figure_jing',
                    'follow_ratio', 'average_repost']  # attribute name
        # baseline that divide attribute number into high part and low part
        baseline = [13, 0.4, 0.6, 10, 5]
        group_num = 10  # group number
        accuary = 0.0  # average accuary
        Sensitivity = 0.0
        Specificity = 0.0

        class att:
            name = ''
            high_spam = 0
            low_spam = 0
            high_nonspam = 0
            low_nonspam = 0
            baseline = 0.0
            num = 0.0
            sum = 0
            spam_sum = 0
            nonspam_sum = 0

        attlist = [att() for i in range(attnum)]  # 包含5个att对象

        for i in range(attnum):
            attlist[i].name = attrname[i]
            attlist[i].baseline = baseline[i]

        for i in range(attnum):
            print(attlist[i].name, attlist[i].baseline)

        rownum = 1
        with open(self.fileNameForTraining, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rownum = rownum + 1
                for i in range(attnum):
                    attlist[i].num = float(row.get(attlist[i].name))
                    is_spam = row.get('is_spammer')
                    if attlist[i].num >= attlist[i].baseline and is_spam == 'yes':
                        attlist[i].high_spam = attlist[i].high_spam + 1
                    elif attlist[i].num < attlist[i].baseline and is_spam == 'yes':
                        attlist[i].low_spam = attlist[i].low_spam + 1
                    elif attlist[i].num >= attlist[i].baseline and is_spam == 'no':
                        attlist[i].high_nonspam = attlist[i].high_nonspam + 1
                    elif attlist[i].num < attlist[i].baseline and is_spam == 'no':
                        attlist[i].low_nonspam = attlist[i].low_nonspam + 1
            for i in range(attnum):
                attlist[i].sum = attlist[i].high_spam + attlist[i].low_spam + \
                    attlist[i].high_nonspam + attlist[i].low_nonspam
                attlist[i].spam_sum = attlist[
                    i].high_spam + attlist[i].low_spam
                attlist[i].nonspam_sum = attlist[
                    i].high_nonspam + attlist[i].low_nonspam

        # spam和nonspam概率
        spam_p = 1.0 * attlist[1].spam_sum / (attlist[1].sum)
        nonspam_p = 1.0 * attlist[1].nonspam_sum / (attlist[1].sum)
        predict_right = 0
        predict_wrong = 0
        tp = 0  # 预测是spam实际也是spam
        tn = 0  # 预测不是spam实际不是spam
        fp = 0  # 预测不是spam实际是spam
        fn = 0  # 预测是spam实际不是spam
        rownum = 1
        with open(self.fileNameForTesting, 'r') as csvfile2:
            reader = csv.DictReader(csvfile2)
            for row in reader:
                rownum = rownum + 1
                ps = 1.0
                pns = 1.0
                for i in range(attnum):
                    cur_num = float(row.get(attlist[i].name))
                    is_spam = row.get('is_spammer')
                    if cur_num >= attlist[i].baseline:
                        ps = ps * \
                            (1.0 * attlist[i].high_spam / attlist[i].spam_sum)
                        pns = pns * \
                            (1.0 * attlist[i].high_nonspam /
                             attlist[i].nonspam_sum)
                    elif cur_num < attlist[i].baseline:
                        ps = ps * \
                            (1.0 * attlist[i].low_spam / attlist[i].spam_sum)
                        pns = pns * \
                            (1.0 * attlist[i].low_nonspam /
                             attlist[i].nonspam_sum)
                # p(x|h)*p(h)
                ps = 1.0 * ps * spam_p
                pns = 1.0 * pns * nonspam_p

                if ps > pns and is_spam == "yes":
                    tp = tp + 1
                elif ps < pns and is_spam == "no":
                    tn = tn + 1
                elif ps <= pns and is_spam == "yes":
                    fp = fp + 1
                elif ps >= pns and is_spam == "no":
                    fn = fn + 1
                predict_right = tp + tn
                predict_wrong = fp + fn
            print(predict_right, predict_wrong)
            accuary = 1.0 * predict_right / \
                (predict_right + predict_wrong) + accuary
            Sensitivity = 1.0 * tp / (tp + fn) + Sensitivity
            Specificity = 1.0 * tn / (fn + tn) + Specificity
        # 10组数据取平均
        print("accuary", accuary / group_num)
        print("sensitivity", Sensitivity / group_num)
        print("specificity", Specificity / group_num)


BayesTools()
