from matplotlib import pyplot as plt

img1 = plt.imread('bin1.png')
img2 = plt.imread('bin2.png')

img1_whites = 0
img2_whites = 0

img1_total = 0
img2_total = 0

for ps in img1:
    for p in ps:
        if p > 0:
            img1_whites += 1
        img1_total += 1

for ps in img2:
    for p in ps:
        if p > 0:
            img2_whites += 1
        img2_total += 1


print("IMG1 RESULT: ", img1_whites, "/", img1_total, "(", (img1_whites/img1_total)*100, "%)")
print("IMG2 RESULT: ", img2_whites, "/", img2_total, "(", (img2_whites/img1_total)*100, "%)")


kwargs = dict(alpha=0.5, density=True, bins=[0,0.5, 1], ec="red")
kwargs2 = dict(alpha=0.5, density=True, bins=[0,0.5, 1], ec="green")
plt.hist(img1, **kwargs)
plt.hist(img2, **kwargs2)

plt.show()
