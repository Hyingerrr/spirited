import os
import deeplake


class DeeplakeClient:
    def __init__(self):
        dataset_path = os.getenv("DATASET_PATH")
        active_loop_token = os.getenv("ACTIVELOOP_TOKEN")
        try:
            self.ds = deeplake.load(dataset_path,read_only=False,token=active_loop_token)
            self.loaded = True
        except Exception as e:
            print(e)
            self.ds = deeplake.empty(dataset_path)
            self.loaded = False


    def save_executor(self, sd_prompts, images: list):
        """
        保存至deeplake
        :param sd_prompts: 绘本每页的prompt
        :type sd_prompts: list
        :param images: 图片集
        :type images: list
        :return:
        :rtype:
        """
        if not self.loaded:
            self.ds.create_tensor('prompts', htype='text')
            self.ds.create_tensor('images', htype='image', sample_compression='png')

        for i, prompt in enumerate(sd_prompts):
            self.ds.append({'prompts': prompt, 'images': deeplake.read(images[i])})