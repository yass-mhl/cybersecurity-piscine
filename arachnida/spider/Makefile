# Définition de l'exécutable
NAME=spider

# Commande par défaut
all: $(NAME)

$(NAME):
	pyinstaller --onefile $(NAME).py

# Nettoyage des fichiers générés
clean:
	rm -rf build dist $(NAME).spec

# Commande pour exécuter le programme (exemple)
run:
	./dist/$(NAME)
