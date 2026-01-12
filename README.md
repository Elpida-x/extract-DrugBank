# deal_DrugBank
用Python的xml.sax库来提取xml文件里面的某些数据。

## Tables
药物基本信息表：**BasicDrug(drugbank-id,name,description)**

药物详细信息表：**DetailedDrug(drugbank-id,synonyms,indication,pharmacodynamics,mechanism-of-action,toxicity,metabolism,absorption,route-of-elimination)**

食物相互作用表：**food-interactions(fid,drugbank-id,food-interaction)**

药物相互作用表：**drug-interactions(drugbank-id,name ,description)**

（实验性质：experimental-properties）

（外部链接：external-links -> 扩展功能-了解更多）

## Test
DrugBank官网下载full database.xml，文件太大传不上，这里只放第一个药物的相关数据用于测试。

https://go.drugbank.com/releases/latest 用学校邮箱发邮件申请即可

## Results
代码如上，对应四个表。结果见rar压缩包。
