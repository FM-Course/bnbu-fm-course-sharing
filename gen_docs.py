######################################
# 文档更新脚本 
#
# author: Jinsui Liu
# email: 3125124390@qq.com
# date: 2025/07/14
#
######################################

import os
from pathlib import Path
import shutil
from pandas import read_csv, DataFrame

def readme_process():
    """
    Find all the readme file in course folders, 
    then copy them to docs with adding file tree.
    """

    def readme_gen(readme_path : Path, folder : Path):
        """
        Copy readme files from course folders to docs path,
        and generate the file tree of course folders.
        """
        try:
            # 读取现有内容
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 生成递归的文件列表部分
            file_list_section = generate_recursive_file_list(folder, base_path=folder)
            
            # 替换或添加文件列表部分
            new_content = content + file_list_section

            # 获取课程名称
            courseName = folder.relative_to(folder.parent)

            
            # 写入更新后的内容
            DashedName = str(courseName).replace(' ', '-')
            docs_path = folder.parent / 'docs' / (DashedName + ".md")
            with open(docs_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print(f"已更新: {docs_path}")
        except Exception as e:
            print(f"处理 {readme_path} 时出错: {e}")

    def generate_recursive_file_list(folder, base_path, indent_level=0):

        """递归生成文件列表部分的Markdown内容"""
        items = []
        indent = "    " * indent_level  # 4个空格作为一级缩进
        
        # 遍历文件夹内容（按字母顺序排序）
        for item in sorted(folder.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            # 忽略readme.md文件本身
            if item.name.lower() == 'readme.md':
                continue
            
            if item.is_dir():
                # 处理目录
                items.append(f"{indent}- 📁 {item.name}/")
                # 递归处理子目录
                items.extend(generate_recursive_file_list(item, base_path, indent_level + 1))
            else:
                # 处理文件
                relatedDIR = str(item.relative_to(current_dir)).replace(' ', '%20').replace('\\','/')
                items.append(f"{indent}- 📄 [{item.name}](https://github.com/FM-Course/bnbu-fm-course-sharing/blob/master/{relatedDIR})")
        
        # 如果是顶级目录且没有内容，添加提示
        if indent_level == 0 and not items:
            items.append("- (空文件夹)")
        
        # 如果是顶级目录，添加标题
        if indent_level == 0:
            return "## 文件列表\n" + "\n".join(items) + "\n"
        else:
            return items

    current_dir = Path(__file__).parent

    for subdir in current_dir.glob('*'):
        if str(subdir.relative_to(current_dir)) == 'docs':
            continue

        if subdir.is_dir():
            readme_path = subdir / "readme.md"
            
            # 检查是否存在readme.md文件（不区分大小写）
            if readme_path.exists():
                readme_gen(readme_path, subdir)

def gen_courselist():
    pass


def generate_mkdocs():
    courseDf = read_csv('./CourseList.csv', index_col=None)
    courseDf = courseDf.replace({'MR' : 0, 'ME' : 1, 'FE' : 2, 'GE' : 3, 'UC' : 4, 'Other' : 5})
    courseDf.sort_values(["Category", "Course Code"], ascending=True, inplace=True)
    
    courseList = [[],[],[],[],[],[]]
    for i in range(len(courseDf)):
        courseList[courseDf.loc[i]['Category']].append(courseDf.loc[i]['Name'])

    categories = ['Major Require','Major Elective','Free Elective','General Education','University Core','Other Meterials']

    courseMarkDownContent = "# 收录课程名录\n"
    for i, type in enumerate(categories):
        courseMarkDownContent += f"## {type}\n"
        for c in courseList[i]:
            courseMarkDownContent += f"- {c}\n"
    
    with open(Path(__file__).parent / "docs" / "list.md", 'w', encoding='utf-8') as f:
        f.write(courseMarkDownContent)
    mkdocsContent = "site_name: BNBU-FM课程攻略\ntheme: readthedocs\nrepo_url: https://github.com/FM-Course/bnbu-fm-course-sharing \n\nnav:\n  - 首页: index.md\n  - 贡献: contribute.md\n  - 收录课程名录: list.md\n  - 致谢: thanks.md\n"

    
    for i, category in enumerate(categories):
        if len(courseList[i]) != 0:
            mkdocsContent += f"  - {category}:\n"
        # mkdocsContent += f"  - {category.replace(' ', '-')}:\n"

        for course in courseList[i]:
            
            DashedName = str(course).replace(' ', '-')
            mkdocsContent += f"    - {course}: {DashedName}.md\n"
    
    with open(Path(__file__).parent / "mkdocs.yml", 'w', encoding='utf-8') as f:
        f.write(mkdocsContent)
    



if __name__ == "__main__":
    readme_process()
    generate_mkdocs()

