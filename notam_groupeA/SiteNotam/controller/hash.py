import hashlib
mdp = 'a' #mdp à chiffrer
mdp = hashlib.sha256(mdp.encode())
mdpC = mdp.hexdigest() #chiffré
print(mdpC)