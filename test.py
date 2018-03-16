likes = [1, 2, 3]
usernames = [3, 4, 5]
amount_of_likes = [6, 7, 8]

z = zip(likes, zip(usernames, amount_of_likes ))

for i, b in z:
    for y, t in b:
        print(i)