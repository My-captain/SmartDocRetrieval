import json
import math

REP_DOC_NUM = 1000
VOC_FILE_PATH = r'static/vocabulary'
DOC_FILE_PATH = r'Spider/doc_detail1.json'
CLUSTER_FILE_PATH = r'static/cluster'
CLASS_NUM = 8

def read_doc_list():
    rep_doc_list = []
    with open(DOC_FILE_PATH, "r", encoding="utf-8") as file:
        doc_list = json.loads(file.read())
        for doc in doc_list[:REP_DOC_NUM]:
            rep_doc_list.append((doc['title'] + '. ' + doc['abstract']).lower())
    return rep_doc_list


def read_voc_list():
    with open(VOC_FILE_PATH, "r", encoding="utf-8") as file:
        voc_list = [i.strip() for i in file.readlines()]
    return voc_list


def calc_idf_list(doc_list, voc_list):
    idf_list = []
    for voc in voc_list:
        counter = 1
        for doc in doc_list:
            if voc in doc:
                counter += 1
        idf_list.append(math.log10(REP_DOC_NUM / counter))
    return idf_list
    #return [math.log10(REP_DOC_NUM / (1 + len([1 for doc in doc_list if voc in doc]))) for voc in voc_list]


def calc_vec_list(doc_list, voc_list, idf_list):
    vec_list = []
    for doc in doc_list:
        vec = []
        for idx, voc in enumerate(voc_list):
            vec.append(doc.count(voc) * idf_list[idx])
        vec_list.append(vec)
    return vec_list
    #return [[doc.count(voc) * idf_list[idx] for idx, voc in enumerate(voc_list)] for doc in doc_list]


def eu_dist_vec_to_vec(v1, v2):
    return math.sqrt(sum([(v1[i] - v2[i])**2 for i in range(len(v1))]))


def cos_dist_vec_to_vec(v1, v2):
    norm_v1 = math.sqrt(sum([(v1[i])**2 for i in range(len(v1))]))
    norm_v2 = math.sqrt(sum([(v2[i])**2 for i in range(len(v1))]))
    return 1 - (math.sqrt(sum([v1[i] * v2[i] for i in range(len(v1))])) / (norm_v1 * norm_v2))


def dist_vec_to_set(v, s, dist_mat):
    return sum([dist_mat[v][e] for e in s]) / len(s)


def cluster_vec(vec_list):
    classifying = [i for i in range(len(vec_list))]
    classes = [[] for i in range(CLASS_NUM)]
    dist_mat = [[0 for j in range(len(vec_list))] for i in range(len(vec_list))]
    max_dist = 0
    c1, c2 = 0, 0
    for i in range(len(vec_list) - 1):
        for j in range(i + 1, len(vec_list)):
            dist = eu_dist_vec_to_vec(vec_list[i], vec_list[j])
            dist_mat[i][j] = dist_mat[j][i] = dist
            if dist > max_dist:
                c1, c2 = i, j
    classes[0].append(c1)
    classes[1].append(c2)
    classifying.pop(classifying.index(c1))
    classifying.pop(classifying.index(c2))
    for i in range(2, len(classes)):
        min_dist_list = [0 for j in range(len(vec_list))]
        for j in classifying:
            min_dist_list[j] = min([dist_vec_to_set(j, k, dist_mat) for k in classes[:i]])
        new_center = min_dist_list.index(max(min_dist_list))
        classes[i].append(new_center)
        classifying.pop(classifying.index(new_center))
    for i in classifying:
        min_dist_list = [dist_vec_to_set(i, k, dist_mat) for k in classes]
        min_dist_class = min_dist_list.index(min(min_dist_list))
        classes[min_dist_class].append(i)
    return classes


def cos_classify(vec, classes, vec_list):
    ave_dist_list = []
    for i in classes:
        ave_dist = sum([cos_dist_vec_to_vec(vec, vec_list[j]) for j in classes[i]]) / len(i)
        ave_dist_list.append(ave_dist)
    return ave_dist_list.index(min(ave_dist_list))


if __name__ == '__main__':
    doc_list = read_doc_list()
    voc_list = read_voc_list()
    idf_list = calc_idf_list(doc_list, voc_list)
    vec_list = calc_vec_list(doc_list, voc_list, idf_list)
    classes = cluster_vec(vec_list)
    for i in classes[1]:
        print(vec_list[i])
    # with open(CLUSTER_FILE_PATH, 'w', encoding='utf-8') as file:
    #     for i in classes:
    #         file.write(str(len(i)) + '\t' + str(i) + '\n')

