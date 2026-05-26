import hashlib
mdp = '5678' #mdp à chiffrer
mdp = hashlib.sha256(mdp.encode())
mdpC = mdp.hexdigest() #chiffré
print(mdpC)
try:
    import pyperclip
    pyperclip.copy(mdpC)
    print("mot de passe copié dans le presse papier!")
except:
    pass
