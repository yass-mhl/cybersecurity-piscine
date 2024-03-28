# Définition de l'exécutable
NAME=spider

# Commande par défaut
all: $(NAME)

$(NAME):
	@echo "Starting build of $(NAME)..."
	@echo -ne '\033[32m                            (0%)\r'
	@sleep 0.2
	@echo -ne '#####                      (33%)\r'
	@pyinstaller --onefile $(NAME).py > /dev/null 2>&1
	@sleep 0.2
	@echo -ne '#############              (66%)\r'
	@sleep 0.2
	@echo -ne '#######################   (100%)\r'
	@echo -ne '\n'
	@echo -e "\033[33mBuild finished"

# Nettoyage des fichiers générés
clean:
	@rm -rf build dist $(NAME).spec images $(NAME) > /dev/null 2>&1
	@echo -ne '\033[36m#######################   (100%)\r'
	@sleep 0.2
	@echo -ne '#############              (66%)\r'
	@sleep 0.2
	@echo -ne '#####                      (33%)\r'
	@sleep 0.2
	@echo -ne '                            (0%)\r'
	@echo -ne '\n'
	@echo "\033[33mClean finished"
