from ocr import *
from docx import Document
import docx2txt
import textract
import os
import re
import pandas as pd
import time

# testing parameters
pdfFile = "Tesseract/Contract_6f.pdf"
txtFile = "Tesseract/Contract_6.txt"
csvFile = "Tesseract/Contract_6c.csv"
contrast = 1.5
size = 1
dpiNum = 300
compOrori = "comp"
lang = "eng"
penalty = 1
page = 11


def get_ocr_data(pdfFile, size, contrast, dpiNum, compOrori, lang):
    # get the dataframe containing the ocr result and data

    print("-----------------------------------")
    print("Getting OCR data")

    start_time = time.time()
    ocr(pdfFile, size, contrast, dpiNum, compOrori, lang)
    ocr_time = time.time() - start_time

    column_name = ["level", "page_num", "block_num", "par_num",
                   "line_num", "word_num", "left", "top", "width",
                   "height", "conf", "text"]
    df_ocr = pd.DataFrame(columns = column_name)
    ocr_data = ocr.data

    for d in ocr_data:
        df_temp = pd.DataFrame.from_dict(d)
        df_ocr = df_ocr.append(df_temp)

    df_ocr = df_ocr[df_ocr.conf != -1]
    word_list = list(df_ocr.text)
    conf_list_temp = list(df_ocr.conf)
    ocr_char_list = []
    conf_list = []

    for i in range(len(word_list)):
        word_list[i] = re.sub('\s+', '', word_list[i])
        for char in word_list[i]:
            if char in {".", "_", "-"}:
                pass
            else:
                ocr_char_list.append(char)
                conf_list.append(conf_list_temp[i])

    return ocr_char_list, ocr_time, conf_list


# need to manually check the txt file with the original word file
def get_word_data_txt(txtFile):
    # get the texts in the txt file and save it to a dataframe

    print("-----------------------------------")
    print("Getting Word Doc data")

    with open(txtFile) as f:
        word_data = f.readlines()

    f.close()

    word_char_list = []

    for para in word_data:
        para = re.sub('\s+', '', para)
        for char in para:
            if char in {".", "_", "-"}:
                pass
            else:
                word_char_list.append(char)

    return word_char_list


def get_csv(txtFile, pdfFile, size, contrast, dpiNum, compOrori, lang):
    # get the data from txt file and ocr result, and save as csv to the same location with the files

    base = os.path.basename(pdfFile)
    file_name = os.path.splitext(base)[0]
    head, tail = os.path.split(pdfFile)

    wlist = get_word_data_txt(txtFile)
    pdflist, ocr_time, conf_list = get_ocr_data(pdfFile, size, contrast, dpiNum, compOrori, lang)

    print("Saving data")
    data = {"word data": wlist, "ocr data": pdflist, "conf": conf_list, "ocr time": [ocr_time]}
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.transpose()

    file_dir = os.path.join(head, file_name)
    path = file_dir + ".csv"
    df.to_csv(path)


# need manual process the csv before passing to result_df function
def result_df(csvFile):
    # return dataframe containing the right data

    df = pd.read_csv(csvFile, encoding= 'unicode_escape')
    df = df[["word data", "ocr data", "check"]]
    df = df.fillna("{}")

    return df


def char_accuracy(csvFile):
    # get the character accuracy of the ocr by comparing with the original word document

    print("-----------------------------------")
    file, extension = os.path.splitext(csvFile)
    print("Character accuracy in", file)

    df = result_df(csvFile)

    num_word_char = len(df["word data"])
    num_ocr_char = len(df["ocr data"])

    error_char_df = df[ df["check"] == 1]
    num_error = error_char_df.shape[0]

    char_accuracy = ((num_word_char - num_error) / num_word_char) * 100
    char_accuracy = round(char_accuracy, 2)

    acc_dict = {"col1": ["Characters predicted", "Errors", "Character accuracy"],
                   "col2": [num_word_char, num_error, char_accuracy]}

    acc_df = pd.DataFrame.from_dict(acc_dict)
    acc_df.columns = ['', '']
    acc_df.index = ['' for _ in range(len(acc_df))]

    print(acc_df)

    return acc_df


def grouped_error(csvFile):
    # return a table of all the error, grouped by the true value

    print("-----------------------------------")
    file, extension = os.path.splitext(csvFile)
    print("Grouped error in", file, "\n")

    df = result_df(csvFile)
    error_char_df = df[ df["check"] == 1]

    miss_char_df = error_char_df[error_char_df["ocr data"] == "{}"]
    num_miss_char = miss_char_df.shape[0]

    grouped_error_df = error_char_df.rename(columns={"word data": "Character",
                                                   "ocr data": "Predicted", "check": "Count_error"})
    grouped_error_df = grouped_error_df.sort_values(by = "Predicted")
    grouped_error_df = grouped_error_df.groupby(["Character", "Predicted"]).sum()

    print(grouped_error_df)
    print("\n", "Note: {} indicates no prediction made by the OCR engine")
    print("Number of missed prediction: ", num_miss_char)

    return grouped_error_df


def accuracy_by_class(csvFile):
    # get the accuracy by character class (lowercase, uppercase, digit, special(punctuations))

    print("-----------------------------------")
    file, extension = os.path.splitext(csvFile)
    print("Accuracy by Character Class in", file, "\n")

    df = result_df(csvFile)

    df_lowercase = df[df["word data"].str.islower()]
    df_uppercase = df[df["word data"].str.isupper()]
    df_digit = df[df["word data"].str.isdigit()]

    iLower = df_lowercase.index
    iUpper = df_uppercase.index
    iDigit = df_digit.index

    df_special = df.drop(index=iLower)
    df_special = df_special.drop(index=iUpper)
    df_special = df_special.drop(index=iDigit)

    num_char = df.shape[0]
    num_lowercase = df_lowercase.shape[0]
    num_uppercase = df_uppercase.shape[0]
    num_digit = df_digit.shape[0]
    num_special = df_special.shape[0]

    num_error = df[df["check"] == 1].shape[0]
    num_error_lowercase = df_lowercase[df_lowercase["check"] == 1].shape[0]
    num_error_uppercase = df_uppercase[df_uppercase["check"] == 1].shape[0]
    num_error_digit = df_digit[df_digit["check"] == 1].shape[0]
    num_error_special = df_special[df_special["check"] == 1].shape[0]

    if num_lowercase != 0:
        lowercase_accuracy = round(((num_lowercase - num_error_lowercase) / num_lowercase) * 100, 2)
    else:
        lowercase_accuracy = 0

    if num_uppercase != 0:
        uppercase_accuracy = round(((num_uppercase - num_error_uppercase) / num_uppercase) * 100, 2)
    else:
        uppercase_accuracy = 0

    if num_digit != 0:
        digit_accuracy = round(((num_digit - num_error_digit) / num_digit) * 100, 2)
    else:
        digit_accuracy = 0

    if num_special != 0:
        special_accuracy = round(((num_special - num_error_special) / num_special) * 100, 2)
    else:
        special_accuracy = 0

    class_type = {"Class_type": ["Lowercase", "Uppercase", "Number", "Symbol"]}
    predicted = {"Count_predicted": [num_lowercase, num_uppercase, num_digit, num_special]}
    error = {"Count_error": [num_error_lowercase, num_error_uppercase, num_error_digit, num_error_special]}
    accuracy = {"Accuracy": [lowercase_accuracy, uppercase_accuracy, digit_accuracy,special_accuracy]}
    report_dict = {**class_type, **predicted, **error, **accuracy}
    report = pd.DataFrame(data = report_dict)

    print("Characters predicted ", num_char)
    print("Errors ", num_error, "\n")
    print(report)

    return report


def throughput(csvFile, page):
    # get the throughput of the ocr

    print("-----------------------------------")
    file, extension = os.path.splitext(csvFile)
    print("Throughput in", file)

    df_original = pd.read_csv(csvFile, encoding= 'unicode_escape')
    ocr_time = df_original["ocr time"][0]
    ocr_time = round(ocr_time, 2)
    avg_ocr_time = round(ocr_time/page, 2)

    df = result_df(csvFile)

    num_word_char = len(df["word data"])
    error_char_df = df[ df["check"] == 1]
    num_error = error_char_df.shape[0]

    throughput_list = []
    penalty_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    for p in penalty_list:
        throughput = ((num_word_char - p * num_error) / ocr_time)
        throughput = round(throughput, 2)
        throughput_list.append(throughput)

    info_dict = {"col1": ["Characters predicted", "Errors", "OCR time", "Page", "OCR time per page"],
                "col2": [num_word_char, num_error, ocr_time, page, avg_ocr_time]}

    info_df = pd.DataFrame.from_dict(info_dict)
    info_df.columns = ['', '']
    info_df.index = ['' for _ in range(len(info_df))]

    throughput_dict = {"Penalty": penalty_list, "Throughput": throughput_list}
    throughput_df = pd.DataFrame.from_dict(throughput_dict)

    print(info_df, "\n")
    print(throughput_df)

    return throughput_df


def accuracy_by_frequency(csvFile):
    # obtain the accuracy of each predicted character by its frequency

    print("-----------------------------------")
    file, extension = os.path.splitext(csvFile)
    print("Accuracy by frequency in", file, "\n")

    df = result_df(csvFile)
    df = df.rename(columns={"word data": "Character",
                            "ocr data": "Predicted", "check": "Error"})
    df = df.sort_values(by="Character")

    pred_df = df.groupby(["Character"]).size().reset_index(name="Count_predicted")
    error_df = df.groupby(["Character"]).sum().reset_index()
    error_df = error_df["Error"]

    frequency_df = pred_df.join(error_df)
    frequency_df = frequency_df.rename(columns={"Error": "Count_error"})

    accuracy = []

    for i in range(0, frequency_df.shape[0]):
        acc = ((frequency_df["Count_predicted"][i] - frequency_df["Count_error"][i]) /
               frequency_df["Count_predicted"][i]) * 100
        acc = round(acc, 2)
        accuracy.append(acc)

    frequency_df["Accuracy_by_frequency"] = pd.Series(accuracy)

    frequency_df.sort_values(by=["Accuracy_by_frequency"], inplace=True)
    frequency_df = frequency_df.reset_index(drop=True)

    print(frequency_df)

    return frequency_df


def error_df(csvFile):
    # return an error dataframe with prediction confidence

    print("-----------------------------------")
    file, extension = os.path.splitext(csvFile)
    print("Error table with prediction confidence for", file, "\n")

    df = pd.read_csv(csvFile, encoding= 'unicode_escape')
    df = df.drop("ocr time", axis=1)

    error_df = df[df["check"] == 1]
    error_df = error_df[["word data", "ocr data", "conf"]]
    error_df = error_df.dropna(subset = ["ocr data"])

    error_df = error_df.rename(columns={"word data": "Character",
                                        "ocr data": "Predicted", "conf": "OCR confidence"})
    error_df = error_df.sort_values(by="OCR confidence")
    error_df = error_df.reset_index()
    error_df = error_df.drop("index", axis=1)

    miss_char_df = error_df[error_df["Predicted"] == "{}"]
    num_miss_char = miss_char_df.shape[0]

    avg_conf = round(error_df["OCR confidence"].mean(), 2)

    print(error_df, "\n")
    print("Average confidence: " ,avg_conf)
    # print("Note: {} indicates no prediction made by the OCR engine")
    # print("Number of missed prediction: ", num_miss_char)

    return error_df


def get_report(csvFile, page):
    # generate evaluation report

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    char_accuracy(csvFile)
    throughput(csvFile, page)
    accuracy_by_class(csvFile)
    accuracy_by_frequency(csvFile)
    grouped_error(csvFile)
    error_df(csvFile)

# run this to get the csv file containing the prediction results
# get_csv(txtFile, pdfFile, size, contrast, dpiNum, compOrori, lang)

# after checked the csv file, run this to get the evaluation
# page: refers to the number of pages ocr-ed
get_report(csvFile, page)

