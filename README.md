# 高级凯撒密码项目说明

## 一、项目简介
本项目为基于凯撒密码的复杂加密算法的V2.0版本，带来了诸多显著改进与新特性，旨在提供更强大、安全且易用的加密解决方案。

## 二、更新内容
1. **UI全面重构**：重新设计了用户界面，使其更加美观、直观，极大地提升了用户体验。
2. **字符支持拓展**：现支持所有字符（当前开放汉字、英文和符号），极大地扩展了加密的应用范围。
3. **加密机制升级**：放弃反向加密方案，采用全新的三轮加密机制，增强了加密的安全性与复杂性。
4. **哈希函数引入**：引入哈希244、哈希256函数，进一步强化加密算法的安全性，有效抵御多种攻击手段。
5. **新增Docker版本**：推出了Docker版本，方便部署与运行，提高了项目的可移植性与环境兼容性。

## 三、算法原理
1. **加密过程**
   - 第一轮加密：根据用户输入的密钥生成偏移序列，基于密钥中字符的ASCII值和其在密钥中的位置。然后针对输入文本中的每个字符，若在允许的字符集内，根据偏移量进行位置移动，生成第一轮加密结果。
   - 第二轮加密：使用SHA - 256对密钥进行扩展，生成新的偏移序列，对第一轮加密结果再次进行类似的加密操作。
   - 第三轮加密：使用SHA - 224对密钥进行扩展，生成新的偏移序列，对第二轮加密结果进行最后一轮加密，得到最终的加密文本。
2. **解密过程**
   - 第三轮解密：先使用SHA - 224扩展密钥生成偏移序列，对加密文本进行反向偏移解密，得到第二轮解密后的中间结果。
   - 第二轮解密：使用SHA - 256扩展密钥生成偏移序列，对中间结果再次反向偏移解密，得到第一轮解密后的结果。
   - 第一轮解密：使用原始密钥生成偏移序列，对第一轮解密后的结果进行最后一次反向偏移解密，恢复出原始文本。

## 四、代码结构
1. **Python版**
   - `generate_allowed_chars`函数：动态生成包含所有汉字及常见符号的字符集。
   - `generate_shifts`函数：根据密钥生成偏移序列。
   - `expand_key_sha256`和`expand_key_sha244`函数：分别使用SHA - 256和SHA - 224扩展密钥并截取指定长度。
   - `encrypt_decrypt_once`函数：执行单轮加密或解密操作。
   - `complex_encrypt`函数：实现三轮加密逻辑。
   - `complex_decrypt`函数：实现三轮解密逻辑，顺序与加密相反。
   - GUI部分：使用`tkinter`库构建图形用户界面，包括输入文本框、密钥输入框、加密和解密按钮以及输出文本框，通过相应的函数实现加密和解密操作的交互逻辑。
2. **Docker版**
   - 文件结构：包含`app.py`（Flask后端代码）、`Dockerfile`（Docker配置文件）、`requirements.txt`（Python依赖）、`templates/index.html`（前端HTML页面）、`docker-compose.yml`（Docker Compose配置）。
   - `app.py`：定义了Flask应用，实现了加密和解密的路由处理函数，与Python版的加密和解密逻辑相同。
   - `templates/index.html`：构建了前端页面，通过JavaScript与后端API进行交互，实现加密和解密操作的用户界面展示和数据传输。
   - `docker-compose.yml`：配置了Docker容器的服务，包括端口映射、卷挂载等。
   - `Dockerfile`：定义了Docker镜像的构建过程，包括安装Python依赖、复制应用程序代码等步骤。

## 五、使用方法
1. **Python版**
   - 确保已安装Python 3.7及以上环境。
   - 运行Python脚本，弹出图形用户界面。
   - 在“输入文本”框中输入要加密或解密的文本，在“密钥”框中输入密钥。
   - 点击“加密”或“解密”按钮，在“输出结果”框中查看相应结果。
2. **Docker版**
   - 确保已安装Docker和Docker Compose。
   - 在项目目录下，执行`docker-compose up`命令构建并启动容器。
   - 打开浏览器，访问`http://localhost:3333`，进入前端页面。
   - 在页面上输入文本和密钥，点击“加密”或“解密”按钮，页面下方显示结果。
   - 为了方便使用，我们已经部署Docker版在我们的服务器上，地址：http://ks.gvicyunjin.cn:3333/

## 六、注意事项
1. 选择密钥时，尽量使用复杂、不易猜测的字符串，以提高加密安全性。
2. 在使用Docker版时，注意检查端口是否被占用，如有冲突需调整端口配置。
3. 对于特殊字符或大量文本的加密解密操作，可能会影响性能，需根据实际需求进行优化或调整。

## 七、开源协议
本项目遵循MIT License开源协议，欢迎大家使用、修改和分发代码，但需保留版权声明和许可声明。

## 八、贡献指南
如果您对本项目感兴趣并希望贡献代码或提出改进建议，欢迎通过以下方式参与：
1. Fork本项目仓库。
2. 创建新的分支进行修改。
3. 提交Pull Request，详细说明您的修改内容和目的。

## 九、联系方式
如果您在使用过程中遇到问题或有任何疑问，可以通过以下方式联系我们：
1. 邮件：2418874224@qq.com
2. GitHub Issue：在项目仓库中创建新的Issue。

## 十、致谢
感谢所有参与本项目的人员，包括开发团队成员（组长：郭子路，成员：龚毅夫，张智宸）以及指导老师薛仙。同时，也感谢使用和关注本项目的用户，希望本项目能为大家在信息安全领域的研究和应用提供一定的帮助。







# Project Description of Advanced_Caesar_V2.0

## I. Project Introduction
This project is the V2.0 version of the complex encryption algorithm based on the Caesar cipher. It brings many significant improvements and new features, aiming to provide a more powerful, secure, and user-friendly encryption solution.

## II. Update Contents
1. **UI Completely Reconstructed**: The user interface has been redesigned to be more beautiful and intuitive, greatly enhancing the user experience.
2. **Expanded Character Support**: Now supports all characters (currently Chinese characters, English, and symbols are enabled), which has greatly expanded the application range of encryption.
3. **Encryption Mechanism Upgraded**: The reverse encryption scheme is abandoned, and a new three-round encryption mechanism is adopted, enhancing the security and complexity of encryption.
4. **Hash Functions Introduced**: The hash244 and hash256 functions are introduced to further strengthen the security of the encryption algorithm and effectively resist various attack means.
5. **Docker Version Added**: A Docker version has been launched, facilitating deployment and operation and improving the portability and environmental compatibility of the project.

## III. Algorithm Principle
1. **Encryption Process**
   - First-round encryption: Generate an offset sequence based on the user-entered key, which is based on the ASCII value of the characters in the key and their positions in the key. Then, for each character in the input text, if it is within the allowed character set, move its position according to the offset to generate the first-round encrypted result.
   - Second-round encryption: Use SHA-256 to expand the key, generate a new offset sequence, and perform a similar encryption operation on the first-round encrypted result again.
   - Third-round encryption: Use SHA-224 to expand the key, generate a new offset sequence, and perform the final round of encryption on the second-round encrypted result to obtain the final encrypted text.
2. **Decryption Process**
   - Third-round decryption: First, use SHA-224 to expand the key to generate an offset sequence, and perform reverse offset decryption on the encrypted text to obtain the intermediate result after the second-round decryption.
   - Second-round decryption: Use SHA-256 to expand the key to generate an offset sequence, and perform reverse offset decryption on the intermediate result again to obtain the result after the first-round decryption.
   - First-round decryption: Use the original key to generate an offset sequence, and perform the final reverse offset decryption on the result after the first-round decryption to restore the original text.

## IV. Code Structure
1. **Python Version**
   - The `generate_allowed_chars` function: Dynamically generates a character set that includes all Chinese characters and common symbols.
   - The `generate_shifts` function: Generates an offset sequence based on the key.
   - The `expand_key_sha256` and `expand_key_sha244` functions: Expand the key using SHA-256 and SHA-224 respectively and truncate it to the specified length.
   - The `encrypt_decrypt_once` function: Performs a single-round encryption or decryption operation.
   - The `complex_encrypt` function: Implements the three-round encryption logic.
   - The `complex_decrypt` function: Implements the three-round decryption logic, which is the reverse of the encryption order.
   - The GUI part: Uses the `tkinter` library to build a graphical user interface, including an input text box, a key input box, encryption and decryption buttons, and an output text box. The corresponding functions implement the interaction logic of the encryption and decryption operations.
2. **Docker Version**
   - File structure: Contains `app.py` (Flask backend code), `Dockerfile` (Docker configuration file), `requirements.txt` (Python dependencies), `templates/index.html` (front-end HTML page), `docker-compose.yml` (Docker Compose configuration).
   - `app.py`: Defines the Flask application and implements the route handling functions for encryption and decryption, which have the same encryption and decryption logic as the Python version.
   - `templates/index.html`: Builds the front-end page and interacts with the back-end API through JavaScript to implement the user interface display and data transmission of the encryption and decryption operations.
   - `docker-compose.yml`: Configures the services of the Docker container, including port mapping, volume mounting, etc.
   - `Dockerfile`: Defines the build process of the Docker image, including installing Python dependencies, copying application code, etc.

## V. Usage
1. **Python Version**
   - Ensure that Python 3.7 or above is installed.
   - Run the Python script, and a graphical user interface will pop up.
   - Enter the text to be encrypted or decrypted in the "Input Text" box and the key in the "Key" box.
   - Click the "Encrypt" or "Decrypt" button and view the corresponding result in the "Output Result" box.
2. **Docker Version**
   - Ensure that Docker and Docker Compose are installed.
   - In the project directory, execute the `docker-compose up` command to build and start the container.
   - Open a browser and visit `http://localhost:3333` to enter the front-end page.
   - Enter the text and key on the page and click the "Encrypt" or "Decrypt" button. The result will be displayed below the page.
   - For the convenience of use, we have deployed the Docker version on our server. The address is: http://ks.gvicyunjin.cn:3333/ 

## VI. Precautions
1. When choosing a key, try to use a complex and hard-to-guess string to improve encryption security.
2. When using the Docker version, pay attention to checking whether the port is occupied. If there is a conflict, adjust the port configuration.
3. For encryption and decryption operations of special characters or a large amount of text, it may affect performance. Optimization or adjustment is required according to actual needs.

## VII. Open Source License
This project follows the MIT License open source license. Everyone is welcome to use, modify, and distribute the code, but the copyright notice and license statement must be retained.

## VIII. Contribution Guide
If you are interested in this project and want to contribute code or make improvement suggestions, you are welcome to participate in the following ways:
1. Fork this project repository.
2. Create a new branch for modifications.
3. Submit a Pull Request, detailing your modification content and purpose.

## IX. Contact Information
If you encounter problems or have any questions during use, you can contact us in the following ways:
1. Email:2418874224@qq.com
2. GitHub Issue: Create a new Issue in the project repository.

## X. Acknowledgments
Thanks to all the personnel involved in this project, including the development team members (Team Leader: Guo Zilu, Members: Gong Yifu, Zhang Zhichen) and the instructor Xue Xian. Also, thanks to the users who use and pay attention to this project. We hope this project can provide some help in the research and application of the information security field.