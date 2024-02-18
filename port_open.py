from os import system, name

port = input("Введите порт: ")

print("\n[!] Не закрывайте это окно [!]\n")

if name == "posix":
	system(f"./bore local {port} --to jetwork.404.mn")
elif name == "nt":
	system(f"bore.exe local {port} --to jetwork.404.mn")
else:
	print("Увы, вероятно Ваша ОС не поддерживается.")
	print("Завершение работы...")
	exit()
