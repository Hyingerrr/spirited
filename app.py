import streamlit as st
from dotenv import load_dotenv

import save_deeplake
from image_pdf import pdf_client
from book_maker import BookMaker
from consts import STYLES, MODLES

load_dotenv('conf.env')


def main():
    st.set_page_config(
        page_title="Spirited generate AI Book",
        page_icon="./images/favicon.ico"
    )
    st.title('📚:violet[S]:orange[Pirited]')
    inputs = st.text_area(":lollipop: 请输入你的描述词，生成一组绘本故事!", max_chars=500,placeholder="请输入你的描述词")

    chapter_num = st.number_input(":strawberry: 页数", min_value=1, max_value=20, value=3)
    # model = st.radio(':strawberry: 选择一个模型', MODLES)
    # if model != "gpt-3.5-turbo-0613":
    #     st.warning("抱歉！目前只支持gpt-3.5-turbo-0613模型，其他模型敬请期待！")
    model = "gpt-3.5-turbo-0613"
    style = st.selectbox(':cherries:选择你喜欢的风格', [key for key in STYLES.keys()])
    is_save = st.checkbox(':banana:是否保存云端')

    if st.button('创作') and inputs:
        # 处理中 暂时放置一段文案
        with st.spinner('请稍等，生成中...'):
            app = BookMaker(inputs, model, STYLES[style], chapter_num)
            # 1. 生成绘本image和description
            # 生成故事描述（含标题）
            story_pages = app.generate_story()

            # 生成SD的Prompt
            app.set_progress(0.25, "正在生成Prompts...")
            app.make_pages_prompt(story_pages)

            # 生成绘本图片页 pageList
            app.set_progress(0.4, '正在创建图像...')
            images_urls = app.text_to_images()

            # 合成一个元组
            pages_images_arr = list(zip(images_urls, story_pages))
            app.set_progress(0.75, '正在转换PDF...')

            # 2. 生成pdf
            pdf_name = app.story_title.replace(" ", "_") + ".pdf".strip('"')
            file_path = app.abspath+"/files/"+pdf_name
            print("PDF文件名：" + file_path)
            pdf_client.pdf_generator(pages_images_arr, file_path)

            st.download_button(label="下载作品", data=file_path, file_name=pdf_name, key='download book')
            st.markdown("<span style='color: rgb(217, 90, 0);'>作品已经生成，您可以点击下载按钮保存</span>", unsafe_allow_html=True)

            # 3. 保存到云端
            if is_save:
                with st.spinner("保存中"):
                    try:
                        app.set_progress(0.85, '正在保存至云端...')
                        ds = save_deeplake.DeeplakeClient()
                        ds.save_executor(app.sd_pages_prompts, app.images_urls)
                    except Exception as e:
                        st.write("出错了，请稍后...", e)

            app.set_progress(1.0, '恭喜完成')
            st.write('创作完成，可以点击下载，也可以保存到云端')
            st.balloons()


if __name__ == "__main__":
    main()
