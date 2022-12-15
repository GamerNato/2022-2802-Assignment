
setosa <- iris[1:50,]
versicolor <- iris[51:100,]
virginica <- iris[101:150,]


boxplot(versicolor["sepal_length"])
boxplot(setosa["sepal_length"])

boxplot(iris$sepal_length~iris$species)
boxplot(iris$sepal_width~iris$species)
boxplot(iris$petal_length~iris$species)
boxplot(iris$petal_width~iris$species)

range(setosa["sepal_length"])
range(setosa["sepal_width"])
range(setosa["petal_length"])
range(setosa["petal_width"])

range(versicolor["sepal_length"])
range(versicolor["sepal_width"])
range(versicolor["petal_length"])
range(versicolor["petal_width"])

range(virginica["sepal_length"])
range(virginica["sepal_width"])
range(virginica["petal_length"])
range(virginica["petal_width"])
