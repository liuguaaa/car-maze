from PIL import Image, ImageSequence

images = [Image.open(f'gif/episode3_screenshot{i}.png') for i in range(88)]  # 假设有10帧

images[0].save('success.gif', save_all=True, append_images=images[1:], optimize=False, duration=200, loop=0)

