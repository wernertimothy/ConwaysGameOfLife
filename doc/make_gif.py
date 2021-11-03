import imageio

images = []
for i in range(10):
    images.append(imageio.imread(f'doc/{i}.png'))
imageio.mimsave('doc/GoL.gif', images)