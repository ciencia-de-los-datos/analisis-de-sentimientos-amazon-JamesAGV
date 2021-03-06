"""
Análisis de Sentimientos usando Naive Bayes
-----------------------------------------------------------------------------------------

El archivo `amazon_cells_labelled.txt` contiene una serie de comentarios sobre productos
de la tienda de amazon, los cuales están etiquetados como positivos (=1) o negativos (=0)
o indterminados (=NULL). En este taller se construirá un modelo de clasificación usando
Naive Bayes para determinar el sentimiento de un comentario.

"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import confusion_matrix

def pregunta_01():
    """
    Carga de datos.
    -------------------------------------------------------------------------------------
    """

    # Lea el archivo `amazon_cells_labelled.tsv` y cree un DataFrame usando pandas.
    # Etiquete la primera columna como `msg` y la segunda como `lbl`. Esta función
    # retorna el dataframe con las dos columnas.
    '''df = ____(
        ____,
        sep=____,
        header=____,
        names=____,
    )

    # Separe los grupos de mensajes etiquetados y no etiquetados.
    df_tagged = ____[____["____"].____()]
    df_untagged = ____[____["____"].____()]

    x_tagged = ____["____"]
    y_tagged = ____["____"]

    x_untagged = ____["____"]
    y_untagged = ____["____"]

    # Retorne los grupos de mensajes'''
    df=pd.read_csv('amazon_cells_labelled.tsv',
                   sep='\t',
                   header=None)
    df.columns=['msg','lbl']
    df_tagged=df[df.lbl.notna()]
    df_untagged=df[df.lbl.isna()]
    x_tagged=df_tagged.msg
    y_tagged=df_tagged.lbl
    x_untagged=df_untagged.msg
    y_untagged=df_untagged.lbl
    return x_tagged, y_tagged, x_untagged, y_untagged   
    return x_tagged, y_tagged, x_untagged, y_untagged


def pregunta_02():
    """
    Preparación de los conjuntos de datos.
    -------------------------------------------------------------------------------------
    """

    # Importe train_test_split
    '''from ____ import ____

    # Cargue los datos generados en la pregunta 01.
    x_tagged, y_tagged, _, _ = pregunta_01()

    # Divida los datos de entrenamiento y prueba. La semilla del generador de números
    # aleatorios es 12345. Use el 10% de patrones para la muestra de prueba.
    x_train, x_test, y_train, y_test = train_test_split(
        ____,
        ____,
        test_size=____,
        random_state=____,
    )

    # Retorne `X_train`, `X_test`, `y_train` y `y_test`'''
    x_tagged, y_tagged, _,_ = pregunta_01()
    x_train, x_test, y_train, y_test = train_test_split(x_tagged, 
                                                    y_tagged, 
                                                    test_size=0.1, 
                                                    random_state=12345)    
    return x_train, x_test, y_train, y_test


def pregunta_03():
    """
    Construcción de un analizador de palabras
    -------------------------------------------------------------------------------------
    """
    # Importe el stemmer de Porter
    # Importe CountVectorizer
    '''from ____ import ____

    # Cree un stemeer que use el algoritmo de Porter.
    stemmer = ____

    # Cree una instancia del analizador de palabras (build_analyzer)
    analyzer = ____().____()

    # Retorne el analizador de palabras'''
    stemmer = PorterStemmer()
    analyzer=CountVectorizer().build_analyzer()
    return lambda x: (stemmer.stem(w) for w in analyzer(x))


def pregunta_04():
    """
    Especificación del pipeline y entrenamiento
    -------------------------------------------------------------------------------------
    """

    # Importe CountVetorizer
    # Importe GridSearchCV
    # Importe Pipeline
    # Importe BernoulliNB
    #from ____ import ____

    # Cargue las variables.
    x_train, _, y_train, _ = pregunta_02()

    # Obtenga el analizador de la pregunta 3.
    analyzer = pregunta_03()
    '''stemmer = PorterStemmer()
    analyzer=CountVectorizer().build_analyzer()
    analizador=lambda x: (stemmer.stem(w) for w in analyzer(x))'''

    # Cree una instancia de CountVectorizer que use el analizador de palabras
    # de la pregunta 3. Esta instancia debe retornar una matriz binaria. El
    # límite superior para la frecuencia de palabras es del 100% y un límite
    # inferior de 5 palabras. Solo deben analizarse palabras conformadas por
    # letras.
    ''''countVectorizer = ____(
        analyzer=____,
        lowercase=____,
        stop_words=____,
        token_pattern=____,
        binary=____,
        max_df=____,
        min_df=____,
    )

    # Cree un pipeline que contenga el CountVectorizer y el modelo de BernoulliNB.
    pipeline = ____(
        steps=[
            ("____", ____),
            ("____", ____()),
        ],
    )

    # Defina un diccionario de parámetros para el GridSearchCV. Se deben
    # considerar 10 valores entre 0.1 y 1.0 para el parámetro alpha de
    # BernoulliNB.
    param_grid = {
        "____": np.____(____, ____, ____),
    }

    # Defina una instancia de GridSearchCV con el pipeline y el diccionario de
    # parámetros. Use cv = 5, y "accuracy" como métrica de evaluación
    gridSearchCV = ____(
        estimator=____,
        param_grid=____,
        cv=____,
        scoring=____,
        refit=____,
        return_train_score=____,
    )

    # Búsque la mejor combinación de regresores
    gridSearchCV.fit(x_train, y_train)

    # Retorne el mejor modelo
    return gridSearchCV'''
    countVectorizer=CountVectorizer(analyzer=analyzer,
                            lowercase=True,
                            stop_words='english',
                            token_pattern=r"(?u)\b\w\w+\b",
                            binary=True,
                            max_df=1.0,
                            min_df=5,)
    #countVectorizer.fit(x_train)
    pipeline=Pipeline(steps=[('vectorizer',countVectorizer),
                            ('model', BernoulliNB())])
    param_grid={'model__alpha':np.linspace(0.1,1.0,10)}
    gridSearchCV=GridSearchCV(estimator=pipeline,
                            param_grid=param_grid,
                            cv=5,
                            scoring='accuracy',
                            return_train_score=True,
                            refit=True)
    gridSearchCV.fit(x_train, y_train)
    return gridSearchCV


def pregunta_05():
    """
    Evaluación del modelo
    -------------------------------------------------------------------------------------
    """

    # Importe confusion_matrix
    #from ____ import ____

    # Obtenga el pipeline de la pregunta 3.
    gridSearchCV = pregunta_04()

    # Cargue las variables.
    X_train, X_test, y_train, y_test = pregunta_02()

    # Evalúe el pipeline con los datos de entrenamiento usando la matriz de confusion.
    cfm_train = confusion_matrix(
        y_true=y_train,
        y_pred=gridSearchCV.predict(X_train),
    )

    cfm_test = confusion_matrix(
        y_true=y_test,
        y_pred=gridSearchCV.predict(X_test),
    )

    # Retorne la matriz de confusion de entrenamiento y prueba
    return cfm_train, cfm_test


def pregunta_06():
    """
    Pronóstico
    -------------------------------------------------------------------------------------
    """

    # Obtenga el pipeline de la pregunta 3.
    gridSearchCV = pregunta_04()

    # Cargue los datos generados en la pregunta 01.
    _, _, X_untagged, _ = pregunta_01()

    # pronostique la polaridad del sentimiento para los datos
    # no etiquetados
    y_untagged_pred = gridSearchCV.predict(X_untagged)

    # Retorne el vector de predicciones
    return y_untagged_pred

#print('Hola Mundo, soy Jaes García')