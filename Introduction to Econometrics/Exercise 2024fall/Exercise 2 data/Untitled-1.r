library("base")

x <- c(21,24,26,27,29,25,25,30)
y <- c(2.8, 3.4, 3.0, 3.5, 3.6, 3., 2.7, 3.7)

relation <- lm(y~x)
print(relation)

