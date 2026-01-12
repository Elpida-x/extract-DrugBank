# deal_DrugBank
用Python的xml.sax库来提取xml文件里面的某些数据。


药物基本信息表：
BasicDrug(drugbank-id,name,description)
drugbank-id 主键
name        药名
description 描述

药物详细信息表：
DetailedDrug(drugbank-id,synonyms,indication,pharmacodynamics,mechanism-of-action,toxicity,metabolism,absorption,route-of-elimination)
drugbank-id          主键/外键
synonyms             同义词
indication           适应症
pharmacodynamics     药效
mechanism-of-action  作用机制
toxicity             毒性/副作用
metabolism           代谢
absorption           吸收
route-of-elimination 消除途径

食物相互作用表：
food-interactions(fid,drugbank-id,food-interaction)

<food-interactions>
 <food-interaction>Avoid echinacea.</food-interaction>
 <food-interaction>Avoid herbs and supplements with anticoagulant/antiplatelet activity. Examples include garlic, ginger, bilberry, danshen, piracetam, and ginkgo biloba.</food-interaction>
</food-interactions>
  

药物相互作用表：
drug-interactions(drugbank-id,name ,description)

<drug-interactions>
    <drug-interaction>
      <drugbank-id>DB06605</drugbank-id>
      <name>Apixaban</name>
      <description>Apixaban may increase the anticoagulant activities of Lepirudin.</description>
    </drug-interaction>
    <drug-interaction>
      <drugbank-id>DB06695</drugbank-id>
      <name>Dabigatran etexilate</name>
      <description>Dabigatran etexilate may increase the anticoagulant activities of Lepirudin.</description>
    </drug-interaction>
    <drug-interaction>
      <drugbank-id>DB01254</drugbank-id>
      <name>Dasatinib</name>
      <description>The risk or severity of bleeding and hemorrhage can be increased when Dasatinib is combined with Lepirudin.</description>
    </drug-interaction>
</drug-interactions>


（实验性质：experimental-properties）
（外部链接：external-links -> 扩展功能-了解更多）