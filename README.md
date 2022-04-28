# 手順

➀Dockerfileをローカルに落とす

➁working directoryを作成する。

➂working directory上でイメージの作成を行う。
「docker build -t jenkins-docker .」を実行する。

➂コンテナの作成を行う。
「docker run -p 8080:8080 -p 50000:50000 -v /var/jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock --name jenkins -d jenkins-docker」を実行する。

＊注意！
以下のようにエラーが出現する可能性がある。
----
touch: cannot touch '/var/jenkins_home/copy_reference_file.log': Permission denied
Can not write to /var/jenkins_home/copy_reference_file.log. Wrong volume permissions?
----
これに対する対処法としては、
「chown -R 1000 /var/jenkins_home」
を実行して、フォルダに対する権限を付与する。

