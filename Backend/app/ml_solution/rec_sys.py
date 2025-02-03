import pickle
import numpy as np
import implicit

path_to_ml_solution = "/code/app/ml_solution"
try:
    with open(path_to_ml_solution + "/model.pkl", "rb") as file:
        model = pickle.load(file)

    with open(path_to_ml_solution + "/sparse.pkl", "rb") as sparse:
        sparse_matrix = pickle.load(sparse)

    with open(path_to_ml_solution + "/person.pkl", "rb") as person:
        person_u = pickle.load(person)

    with open(path_to_ml_solution + "/items.pkl", "rb") as item:
        thing_u = pickle.load(item)

    with open(path_to_ml_solution + "/item_frequency.pkl", "rb") as freq_file:
        item_probabilities = pickle.load(freq_file)
except Exception as e:
    print([f"Error: {e}"])

def get_rec(uid_for_rec, n_rec):
    def recommend_for_new_user(item_probabilities, n_rec):
        items = list(item_probabilities.keys())
        probabilities = list(item_probabilities.values())
        recommendations = np.random.choice(items, size=n_rec, replace=False, p=probabilities)
        return recommendations

    try:
        user_index = person_u.index(uid_for_rec)
    except ValueError:
        recommendations = recommend_for_new_user(item_probabilities, n_rec)
        print("Холодный старт")
        return [f"{item}" for item in recommendations]

    recomendation = model.recommend(
        user_index,
        sparse_matrix,
        N=n_rec,
        filter_already_liked_items=False,
    )

    rec_array = []
    for i in range(n_rec):
        rec_array.append(int((thing_u[recomendation[0][i]])))
    print(rec_array)
    return rec_array



def get_similar_items(item_id, n_similar):
    try:
        # Загрузка модели и данных
        with open(path_to_ml_solution + "/model.pkl", "rb") as file:
            model = pickle.load(file)

        # Находим похожие товары
        result = model.similar_items(item_id, N=n_similar)

        return result

    except Exception as e:
        return [f"Ошибка: {e}"]
