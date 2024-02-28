from os import system, name
from network import port_gen

port = input("Введите порт: ")
dest = port_gen(7000, 9000)

print(f"\nУдалённый ПОРТ: {dest}")
print("\n[!] Не закрывайте это окно [!]\n")

if name == "posix":
	system(f"./bore local {port} --to jetwork.404.mn --port {dest}")
elif name == "nt":
	system(f"bore.exe local {port} --to jetwork.404.mn --port {dest}")
else:
	print("Увы, вероятно Ваша ОС не поддерживается.")
	print("Завершение работы...")
	exit()
