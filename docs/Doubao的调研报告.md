# 基于双曲语义空间的数学性质预测研究综述与实验设计

## 1. 研究背景与理论基础

### 1.1 双曲几何在知识表示中的优势

双曲几何作为一种具有恒定负曲率的非欧几何空间，在处理层次结构数据方面展现出独特优势。与欧氏空间的多项式体积增长不同，双曲空间具有指数体积增长特性，这使其能够以较低的维度高效表示大规模层次结构数据[(64)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11625262/)。在庞加莱球模型中，双曲 n - 空间 Hⁿ被表示为ℝⁿ中的开单位球：Hⁿ = {x ∈ ℝⁿ : ||x|| < 1}，其中空间中每一点 (x, y) 都有一个 "放大系数"λ = 2/(1 - r²)，r² = x² + y²[(34)](https://wenku.csdn.net/column/5643c9f63j)。

双曲空间的这种几何特性使其特别适合表示具有层次结构的知识图谱。知识图谱通常表现出层次化和逻辑化的模式，这些模式必须在嵌入空间中得到保持。对于层次化数据，双曲嵌入方法已经显示出高保真度和简洁表示的前景[(12)](https://arxiv.org/pdf/2005.00545)。与欧氏空间相比，双曲空间能够以更少的维度实现更好的表示质量，特别是在处理树状结构数据时，双曲嵌入可以实现任意低的失真度而无需优化[(57)](https://pubmed.ncbi.nlm.nih.gov/31131375/)。

### 1.2 双曲图神经网络的技术进展

双曲图神经网络（HGNN）的发展经历了从基本几何适应到复杂多空间框架的演进过程。早期的 HyperGCN 通过将欧氏图卷积网络推广到双曲空间，引入了特征变换、邻域聚合和非线性激活三个不同的层[(52)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9997089/)。随后的研究提出了更复杂的架构，如 LGIN（Lorentzian Graph Isomorphic Network），这是一种专门设计用于在洛伦兹双曲空间模型中实现增强判别能力的新型 GNN[(3)](https://arxiv.org/pdf/2504.00142v3)。

在邻域聚合技术方面，双曲邻域聚合利用双曲空间来聚合图中相邻节点的信息，这一过程可以大致分为两个主要步骤：邻域权重计算和均值聚合计算。最新的研究还探索了基于偏微分方程的方法，如 Hyperbolic-PDE GNN，它利用微分方程的解作为节点嵌入空间，提出了一种基于双曲偏微分方程组的图神经网络[(2)](https://arxiv.org/html/2505.23014v1/)。

在理论分析方面，研究人员提出了节点特定空间选择方法，通过局部几何双曲性来优化图神经网络的性能[(4)](https://object.cloud.sdsc.edu/v1/AUTH_da4962d3368042ac8337e2dfdd3e7bf3/ml-papers/TMLR/2024/nodespecific_space_selection_via_localized_geometric_hyperbolicity_in_graph_neural_networks__f2061013.pdf)。这些方法能够根据图结构的局部特性自适应地选择最优的双曲空间参数，从而提高模型的表达能力和泛化性能。

### 1.3 数学知识图谱的表示挑战

数学知识表示面临着独特的挑战，主要体现在其复杂的层次结构和丰富的语义关系上。Lean Mathlib 作为一个用户维护的 Lean 定理证明器数学库，涵盖了广泛的数学领域，其 monolithic 统一组织结构使其成为神经定理证明数据集的优秀基础[(102)](https://mathai-iclr.github.io/papers/papers/MATHAI_23_paper.pdf?utm_campaign=The%20Batch\&utm_medium=email&_hsmi=152811001&_hsenc=p2ANqtz-_LGI8t74DqPz9W0rAv4KpiJXiadiw0VPPu2n1V0GcXHVDD0bgrM4l6DJalvwvOpVUv4vIP02pnW3Dcg4fgQbsG4_4rWw\&utm_content=152811001\&utm_source=hs_email)。然而，传统的欧氏空间表示方法在处理数学知识的层次结构时遇到了 "维度爆炸" 问题 —— 要么信息挤在一起分不清，要么需要成百上千维才能勉强表示[(50)](https://wenku.csdn.net/column/4kjkno7mde)。

在数学定理证明中，前提选择是一个关键瓶颈，现有的基于语言的方法往往孤立地处理前提，忽略了连接它们的依赖关系网络[(70)](https://arxiv.org/pdf/2510.23637)。此外，数学概念的定义往往具有复杂的依赖关系，形成了庞大的有向无环图（DAG）结构。这些挑战使得传统的欧氏空间表示方法难以有效捕捉数学知识的内在结构。

## 2. 相关研究现状分析

### 2.1 双曲嵌入在数学领域的应用

双曲嵌入在数学领域的应用主要集中在知识图谱补全和定理证明两个方面。在知识图谱补全任务中，研究人员提出了多种双曲知识图谱嵌入模型。Hyperbolic Knowledge Graph Embeddings 通过利用双曲几何为层次结构提供高质量嵌入，在标准知识图谱基准测试中显示出显著优势[(17)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7250606/pdf/978-3-030-49461-2_Chapter_12.pdf)。更进一步，研究人员提出了层次化双曲知识图谱嵌入（HypH-KGE），通过设计基于注意力的可学习曲率来保持丰富的语义层次结构[(15)](https://arxiv.org/pdf/2204.13704v1)。

在定理证明方面，双曲嵌入技术被应用于增强推理能力。研究人员提出了一种双曲知识图谱嵌入模型，能够同时捕获层次化和逻辑化模式，结合双曲反射和旋转与注意力机制来建模复杂的关系模式[(69)](https://aclanthology.org/anthology-files/anthology-files/anthology-files/pdf/acl/2020.acl-main.617.pdf)。实验结果表明，该方法在低维度下的平均倒数排名（MRR）比之前的欧氏和双曲方法提高了 6.1%。

在数学概念表示方面，Graph2Tac 提出了一种图神经网络，具有构建新定义层次表示的新颖方法，其在线定义任务实现了 1.72 倍的改进[(25)](https://research.ibm.com/publications/graph2tac-online-representation-learning-of-formal-math-concepts)。该模型能够学习数学概念的层次结构表示，为数学性质预测提供了基础。

### 2.2 图神经网络在数学定理证明中的应用

图神经网络在数学定理证明中的应用已经取得了显著进展。Graph2Tac 作为一个图神经网络，使用新颖的方法为新定义构建层次表示，其在线表示学习任务实现了相对于离线等价方法 72 倍的改进[(25)](https://research.ibm.com/publications/graph2tac-online-representation-learning-of-formal-math-concepts)。该模型的核心创新在于能够动态学习数学概念的层次结构，适应不同数学领域的概念表示需求。

在高阶逻辑证明搜索方面，研究人员首次将图神经网络用于高阶证明搜索，并证明了 GNN 能够改进该领域的最先进结果[(20)](https://research.google/pubs/graph-representations-for-higher-order-logic-and-theorem-proving/)。这一突破表明，图神经网络在处理复杂的数学逻辑结构方面具有巨大潜力。

Nazrin 系统是另一个重要进展，它是一个基于图神经网络的定理证明代理，使用原子策略和 ExprGraph 数据结构。Nazrin 通过专门调度原子策略来规避现有证明代理面临的许多挑战，并且足够鲁棒，可以在消费级硬件上进行训练和评估[(21)](https://arxiv.org/html/2602.18767v2)。该系统的 ExprGraph 数据结构为 Lean 表达式提供了简洁的表示，能够有效捕捉数学表达式的结构特征。

在推理框架方面，研究人员提出了 GraphMind，这是一个新颖的基于动态图的框架，将图神经网络与大语言模型集成，用于迭代选择定理并生成多步推理的中间结论[(23)](https://www.arxiv.org/pdf/2511.19078)。该框架采用 GNN 对当前推理状态进行编码，并支持基于语义的上下文感知定理选择，为复杂数学推理提供了强大的工具。

### 2.3 Lean Mathlib 相关研究进展

Lean Mathlib 作为现代数学形式化的重要平台，其相关研究涵盖了数据提取、证明生成和机器学习应用等多个方面。在数据提取方面，研究人员开发了专门的工具从 Lean 库（特别是 Mathlib）中提取数据，这些工具主要关注可能对训练机器学习模型有用的数据[(105)](https://github.com/kim-em/lean-training-data)。

LeanDojo 是一个重要的数据处理工具，它能够追踪 Lean 项目并提取丰富的语法 / 语义信息。追踪过程首先追踪整个 Lean 仓库，结果是包含丰富语法 / 语义信息的追踪仓库、文件和定理，这些信息在源代码中不易获得但对下游任务有用，包括但不限于策略状态、策略和策略中的前提[(108)](https://leandojo.readthedocs.io/en/latest/user-guide.html)。

在证明生成方面，研究人员提出了通过探索状态转换图生成数百万个带证明的 Lean 定理的方法。MIL 作为 Mathlib 的官方教程，包含许多涵盖群论、拓扑和数论等高级领域的定理[(98)](https://www.arxiv.org/pdf/2503.04772)。这种大规模的定理数据集为机器学习模型的训练提供了丰富的资源。

在定理难度评估方面，研究人员开发了 LeanProgress 系统，通过证明进度预测来指导神经定理证明搜索。该系统在 Mathlib 4 上相比基线性能 41.4% 有 8% 的改进，特别是对于较长的证明[(101)](https://arxiv.org/pdf/2502.17925v3)。这些结果表明，证明进度预测可以增强自动化和交互式定理证明，使用户能够对证明策略做出更明智的决策。

### 2.4 研究现状总结与差距分析

基于上述文献调研，当前研究在双曲空间表示和数学定理证明方面已经取得了重要进展，但仍存在以下研究差距：



1. **理论基础的系统性不足**：虽然双曲几何在层次结构表示方面的优势已被广泛认可，但将其系统应用于数学性质预测的理论框架尚不完善，特别是缺乏对数学对象代数 / 拓扑性质在双曲空间中几何意义的深入分析。

2. **"层级爆炸" 问题的解决方案有限**：现有的双曲嵌入方法主要针对一般知识图谱，对于数学定义中特有的 "层级爆炸" 问题（即定义依赖关系的指数级增长）缺乏专门的解决方案。虽然 UHCone 等方法能够捕获隐式层次结构，但在处理数学概念的复杂依赖关系方面仍有改进空间。

3. **显式特征维度分析的缺失**：当前研究主要关注双曲嵌入的几何性质，但对如何从嵌入中提取和分析显式特征维度以预测数学性质的研究较少。这一缺失限制了模型的可解释性和预测能力。

4. **大规模数学数据处理能力不足**：虽然已有工具能够处理 Mathlib 数据，但在构建大规模、高质量的数学性质预测数据集方面仍存在挑战，特别是在标注数学对象的代数 / 拓扑性质方面。

5. **模型泛化能力有待提升**：现有模型在特定数学领域表现良好，但在跨领域泛化和处理新定义方面的能力有限，需要更强的在线学习和适应能力。

## 3. 研究假设与创新点评估

### 3.1 核心研究假设验证

本研究的核心假设是：数学对象的代数 / 拓扑性质在双曲嵌入空间中是线性可分或具有特定聚类结构。这一假设基于以下理论基础：

**代数性质的几何解释**：在双曲空间中，具有相似代数结构的数学对象（如群、环、域等）应该形成紧密的聚类。例如，交换群和非交换群可能在双曲空间中形成不同的聚类，而子群关系可能表现为包含关系的几何结构。

**拓扑性质的空间分布**：具有相同拓扑性质的数学对象（如连通性、紧致性、维度等）应该在双曲空间中表现出相似的几何特征。拓扑等价的对象可能位于相近的区域，而拓扑不同的对象则相距较远。

**层次结构的自然嵌入**：数学定义的层次关系（如从集合论基础到高级数学概念的构建）在双曲空间中应该得到自然的几何表示。父概念的嵌入应该包含子概念的嵌入，形成类似树状的层次结构。

为验证这一假设，我们将设计以下实验：



1. **线性可分性测试**：使用支持向量机（SVM）在双曲嵌入空间中测试不同数学性质类别的线性可分性。

2. **聚类分析**：应用层次聚类和 k-means 聚类算法，验证具有相同性质的数学对象是否形成紧密聚类。

3. **流形学习**：使用 t-SNE 和 UMAP 等降维技术可视化双曲嵌入空间，观察不同性质类别的分布模式。

4. **距离分析**：计算同一性质类别内和不同性质类别间的双曲距离分布，验证类内紧凑性和类间分离性。

### 3.2 创新点一：双曲空间解决层级爆炸问题

**创新点描述**：传统的欧氏空间表示方法在处理数学定义的层次结构时面临 "层级爆炸" 问题，即随着定义层次的增加，所需的表示维度呈指数级增长。本研究提出利用双曲空间的指数体积增长特性来自然容纳这种层次复杂性，通过双曲嵌入将指数级增长的定义空间映射到低维双曲空间中，从而解决维度爆炸问题。

**技术路线**：



1. **定义依赖图构建**：从 Lean Mathlib 中提取数学定义及其依赖关系，构建有向无环图（DAG）。

2. **双曲嵌入学习**：使用 HyperGCN 或类似模型学习定义的双曲嵌入，利用双曲空间的几何性质捕获层次关系。

3. **层次结构保持**：通过设计专门的损失函数，确保父定义的嵌入在几何上包含子定义的嵌入，形成自然的层次结构。

4. **复杂度分析**：对比双曲嵌入与欧氏嵌入在表示相同层次结构时所需的维度数和计算复杂度。

**预期效果**：



* 将数学定义的层次结构压缩到低维双曲空间（预计 10-30 维）

* 保持层次关系的几何意义，父概念包含子概念

* 显著降低存储和计算复杂度，解决 "层级爆炸" 问题

* 提高模型在处理大规模数学知识库时的效率

### 3.3 创新点二：显式特征维度分析

**创新点描述**：现有双曲嵌入方法通常将嵌入向量作为黑盒使用，缺乏对各个维度语义含义的明确解释。本研究提出 "显式特征维度" 分析方法，通过数学性质的先验知识指导嵌入学习过程，使每个维度对应特定的数学属性或概念，从而提高模型的可解释性和预测能力。

**技术路线**：



1. **特征维度设计**：根据数学性质分类（如代数结构、拓扑性质、分析性质等）设计初始特征维度。

2. **语义监督学习**：使用数学性质标注数据，通过多任务学习机制引导不同维度捕获特定性质。

3. **维度重要性评估**：通过注意力机制或梯度分析评估各维度对不同性质预测的贡献度。

4. **维度解释框架**：建立从嵌入维度到数学概念的映射关系，提供可解释的预测结果。

**预期效果**：



* 每个嵌入维度具有明确的数学语义解释

* 提高性质预测的准确率和可解释性

* 为数学概念的语义分析提供新的工具

* 支持对未知数学对象性质的快速推断

## 4. 第一阶段实验设计（数据工程）

### 4.1 数据获取与预处理流程

**数据来源与范围**：本阶段的数据获取主要集中在 Lean Mathlib 4 仓库，重点关注其中的数学定义、定理和证明。根据 Mathlib 的组织结构，我们将按数学领域进行分层采样，包括基础数学（集合论、逻辑学）、代数结构（群论、环论、域论）、分析学（实分析、复分析）、拓扑学等核心领域[(102)](https://mathai-iclr.github.io/papers/papers/MATHAI_23_paper.pdf?utm_campaign=The%20Batch\&utm_medium=email&_hsmi=152811001&_hsenc=p2ANqtz-_LGI8t74DqPz9W0rAv4KpiJXiadiw0VPPu2n1V0GcXHVDD0bgrM4l6DJalvwvOpVUv4vIP02pnW3Dcg4fgQbsG4_4rWw\&utm_content=152811001\&utm_source=hs_email)。

**数据提取工具选择**：我们将使用 LeanDojo 作为主要的数据提取工具，因为它能够追踪 Lean 项目并提取丰富的语法 / 语义信息。LeanDojo 的追踪过程包括：首先追踪整个 Lean 仓库，生成包含丰富语法 / 语义信息的追踪仓库、文件和定理，这些信息在源代码中不易获得但对下游任务有用，包括策略状态、策略和策略中的前提[(108)](https://leandojo.readthedocs.io/en/latest/user-guide.html)。同时，我们将使用 kim-em/lean-training-data 仓库提供的工具进行补充数据提取，这些工具专门用于从 Lean 库中提取对机器学习模型训练有用的数据[(105)](https://github.com/kim-em/lean-training-data)。

**数据预处理步骤**：



1. **原始数据清洗**：去除无效或重复的定义，标准化命名规范，统一数据格式。

2. **语法解析**：使用 Lean 的抽象语法树（AST）解析器将.lean 文件转换为结构化数据，提取定义、定理、证明等关键元素。

3. **语义标注**：为每个定义标注其数学领域、类型签名、主要性质（如交换性、结合性、连续性等）。

4. **依赖关系提取**：分析定义之间的导入关系和依赖关系，构建定义依赖图。

5. **性质标签生成**：基于数学知识手动或半自动标注每个定义的代数 / 拓扑性质，建立性质标签体系。

**质量控制措施**：



* 建立数据验证机制，确保提取的定义和证明的正确性

* 实施数据去重和一致性检查

* 对标注的性质标签进行交叉验证，确保标注质量

* 建立数据版本控制系统，跟踪数据变更历史

### 4.2 数学定义依赖图谱构建

**图结构定义**：数学定义依赖图谱 G = (V, E)，其中：



* 顶点集 V：包含所有数学定义、定理、常数等数学对象

* 边集 E：包含三种类型的有向边

1. **定义依赖边**：从被依赖的定义指向依赖它的定义

2. **定理使用边**：从被引用的定理指向使用它的定理或证明

3. **类型继承边**：从父类型指向子类型，表示类型层次关系

**节点特征设计**：每个节点包含以下特征：



1. **基础信息**：名称、数学领域、定义类型（函数、常数、类型等）

2. **语法特征**：参数数量、表达式复杂度、抽象层次

3. **语义特征**：类型签名、主要性质标签、相关概念

4. **结构特征**：在依赖图中的入度、出度、层次深度

**边特征设计**：每条边包含以下特征：



1. **依赖类型**：直接依赖、间接依赖、继承关系

2. **依赖强度**：基于使用频率和重要性的权重

3. **语义关系**：等价、蕴含、包含等逻辑关系

**构建算法流程**：



1. **初始图构建**：从 Lean 源文件中提取所有定义和定理，建立初始节点集合

2. **依赖关系识别**：分析每个定义的导入语句和引用关系，建立依赖边

3. **类型层次构建**：基于类型系统构建继承关系图

4. **图优化**：去除冗余边，合并等价节点，优化图结构

### 4.3 性质标签体系设计

**标签分类体系**：我们设计了一个多层次的数学性质标签体系，包括：

**一级分类（领域类别）**：



* 代数性质：交换性、结合性、分配律、逆元存在性等

* 拓扑性质：连通性、紧致性、可分性、维数等

* 分析性质：连续性、可微性、可积性、收敛性等

* 序性质：偏序、全序、良序、格性质等

**二级分类（具体性质）**：



* 群论性质：阿贝尔群、循环群、有限群、单群等

* 环论性质：交换环、整环、除环、诺特环等

* 拓扑空间性质：豪斯多夫空间、正规空间、度量空间等

* 函数性质：双射、单射、满射、同态、同构等

**标签标注策略**：



1. **自动标注**：基于定义的语法结构和类型签名自动推断部分性质

2. **规则匹配**：使用预定义的规则集匹配已知的性质模式

3. **人工验证**：由数学专业人员对自动标注结果进行验证和补充

4. **交叉验证**：通过多个标注者的独立标注结果进行一致性检验

**标签置信度评估**：



* 自动标注：置信度 0.6-0.8（基于规则覆盖率和匹配强度）

* 规则匹配：置信度 0.7-0.9（基于规则的准确性）

* 人工标注：置信度 0.9-1.0（基于专家知识）

### 4.4 数据质量控制与版本管理

**质量控制流程**：



1. **数据完整性检查**：确保所有定义都有完整的依赖关系记录

2. **语法正确性验证**：使用 Lean 编译器验证提取的定义语法正确性

3. **逻辑一致性检查**：检查依赖关系图中是否存在循环依赖和逻辑矛盾

4. **性质标签一致性**：验证性质标签与定义内容的一致性

**版本管理策略**：



1. **Git 版本控制**：使用 Git 管理数据工程过程中的所有变更

2. **数据版本标记**：为每个版本的数据生成唯一标识和变更日志

3. **备份策略**：定期备份处理后的数据，确保数据安全

4. **协作规范**：建立数据处理的标准化流程和质量标准

**数据存储架构**：



* 原始数据：存储在 Git 仓库中，保持与 Lean Mathlib 的同步

* 中间数据：存储在关系型数据库中，便于查询和分析

* 处理后数据：存储为图格式文件（如 GraphML、JSON），便于图算法处理

* 标注数据：存储为结构化数据集，支持机器学习模型训练

## 5. 欧拉常数 γ 案例研究

### 5.1 欧拉常数 γ 的数学定义与性质

**基本定义**：欧拉 - 马歇罗尼常数 γ（Euler-Mascheroni constant）是数学分析和数论中一个重要的数学常数，通常用小写希腊字母 γ 表示。它定义为调和级数与自然对数的极限差：

γ = lim(n→∞)(1 + 1/2 + 1/3 + ... + 1/n - ln(n))

该常数的数值，精确到 50 位小数为：0.57721 56649 01532 86060 65120 90082 40243 10421 59335 93992...[(138)](https://en-academic.com/dic.nsf/enwiki/102308/29977)

**数学性质**：



1. **级数表示**：γ 可以表示为无穷级数 γ = Σ(k=1 到∞)(1/k - ln (1+1/k))

2. **积分表示**：γ 有多种积分表示形式，如 γ = -∫₀^∞ e^(-x) ln (x) dx

3. **与 γ 函数的关系**：γ 是 γ 函数的导数在 1 处的值：γ = ψ(1) = Γ'(1)/Γ(1)

4. **与黎曼 ζ 函数的关系**：γ 是黎曼 ζ 函数在 s=1 处的洛朗展开式的常数项

**在 Lean Mathlib 中的定义**：在 Lean Mathlib 4 中，欧拉常数的定义位于 Mathlib/NumberTheory/Harmonic/EulerMascheroni.lean 文件中。该实现定义了两个序列：



* eulerMascheroniSeq (n) = harmonic (n) - log (n+1)（严格递增序列）

* eulerMascheroniSeq'(n) = harmonic (n) - log (n)（严格递减序列）

通过证明这两个序列收敛到共同的极限 γ，并给出了 1/2 < γ < 2/3 的界。

### 5.2 欧拉常数在 Lean Mathlib 中的表示形式

**定义结构分析**：在 Lean 中，欧拉常数的定义采用了构造性的方法，通过两个辅助序列的极限来定义 γ：



```
/-! # The Euler-Mascheroni constant \`γ\` -/

namespace Real

/- The sequence with \`n\`-th term \`harmonic n - log (n + 1)\`. -/

noncomputable def eulerMascheroniSeq (n : ℕ) : ℝ := harmonic n - log (n + 1)

/- The sequence with \`n\`-th term \`harmonic n - log n\`. -/

noncomputable def eulerMascheroniSeq' (n : ℕ) : ℝ := if n = 0 then 2 else harmonic n - log n

/- The Euler-Mascheroni constant \`γ\`. -/

noncomputable def eulerMascheroniConstant : ℝ := limUnder atTop eulerMascheroniSeq

end Real
```

**证明结构分析**：Lean Mathlib 中的证明包含以下关键步骤：



1. 证明 eulerMascheroniSeq 是严格递增序列

2. 证明 eulerMascheroniSeq' 是严格递减序列

3. 证明两个序列的差趋向于 0

4. 由此得出两个序列收敛到共同的极限 γ

5. 计算具体的数值界：1/2 < γ < 2/3

**依赖关系分析**：欧拉常数的定义依赖于以下数学概念：



* 自然数（ℕ）和实数（ℝ）的基本性质

* 调和级数（harmonic）的定义和性质

* 自然对数（log）函数的定义和性质

* 极限（limUnder）的定义和收敛性理论

* 序列的单调性和收敛性分析

### 5.3 基于双曲空间的性质预测验证

**实验设计**：我们将以欧拉常数 γ 为例，验证基于双曲空间的数学性质预测方法的有效性。

**特征提取**：从欧拉常数的 Lean 定义中提取以下特征：



1. **结构特征**：定义的语法结构、参数类型、表达式复杂度

2. **依赖特征**：直接依赖的数学概念（harmonic, log 等）

3. **性质特征**：已知的数学性质（如常数性、实数性、近似值等）

4. **上下文特征**：定义所在的数学领域（数论、分析）

**双曲嵌入学习**：



1. 将欧拉常数的定义及其依赖关系构建为图结构

2. 使用 HyperGCN 模型学习图中各节点的双曲嵌入

3. 特别关注 γ 节点与其依赖节点（harmonic, log 等）的几何关系

**性质预测验证**：



1. **已知性质验证**：验证模型是否能从双曲嵌入中正确预测 γ 的基本性质（如实数、常数、介于 1/2 和 2/3 之间等）

2. **未知性质推断**：尝试从嵌入中推断 γ 的其他性质（如无理数性、超越性等，尽管这些在当前数据中可能未标注）

3. **相似性分析**：找出在双曲空间中与 γ 最相似的其他数学常数（如 π, e 等），分析它们的共同性质

**实验预期结果**：



1. γ 节点在双曲空间中应该与其他数学常数（如 π, e）形成一个小聚类

2. γ 的嵌入应该靠近其依赖概念（harmonic, log）的嵌入

3. 模型应该能够正确预测 γ 的已知数值性质

4. 嵌入空间应该反映 γ 在数学分析中的核心地位

### 5.4 案例研究的推广意义

**方法论贡献**：欧拉常数案例研究为基于双曲空间的数学性质预测方法提供了重要的验证和示范：



1. **可行性验证**：证明了该方法能够有效处理具体的数学常数定义，并正确预测其性质

2. **方法优化**：通过案例研究发现了方法的优势和不足，为后续改进提供了方向

3. **工具验证**：验证了所使用的图构建、嵌入学习和性质预测工具的有效性

**推广应用**：该案例的成功经验可以推广到其他数学对象：



1. **数学常数**：π, e, φ（黄金分割比）等其他重要常数

2. **特殊函数**：Γ 函数、ζ 函数、贝塞尔函数等

3. **代数结构**：群、环、域等抽象代数对象

4. **拓扑空间**：各种拓扑空间和流形

**理论意义**：案例研究为理解数学概念在双曲空间中的几何表示提供了具体实例，有助于建立数学语义与几何结构之间的桥梁，为数学知识的机器理解和推理提供新的理论基础。

## 6. 研究路线图与里程碑设置

### 6.1 整体研究路线图

基于用户提供的时间规划，我们制定了详细的研究路线图，分为四个主要阶段：

**第一阶段：数据工程（1-3 月，共 13 周）**



* 第 1-2 周：项目启动，文献调研，确定数据范围

* 第 3-5 周：数据获取工具配置，Lean Mathlib 数据提取

* 第 6-8 周：数据清洗，语法解析，基础数据结构构建

* 第 9-11 周：依赖关系提取，图结构构建

* 第 12-13 周：性质标签体系设计，初步标注，质量检查

**第二阶段：模型构建（4-7 月，共 17 周）**



* 第 14-16 周：双曲图神经网络架构设计，基准模型实现

* 第 17-19 周：嵌入学习算法开发，训练策略制定

* 第 20-22 周：性质预测模块设计，多任务学习框架构建

* 第 23-25 周：模型训练，超参数调优，初步评估

* 第 26-29 周：模型优化，对比实验，性能分析

**第三阶段：几何语义分析（8-10 月，共 13 周）**



* 第 30-32 周：双曲空间几何性质分析，线性可分性验证

* 第 33-35 周：聚类结构分析，相似性度量研究

* 第 36-38 周：显式特征维度设计，维度语义解释

* 第 39-41 周：案例研究深入，欧拉常数等具体对象分析

* 第 42 周：中期总结，结果分析，问题识别

**第四阶段：论文写作（11-12 月，共 9 周）**



* 第 43-45 周：研究成果整理，实验数据汇总

* 第 46-48 周：论文初稿撰写，图表制作

* 第 49-50 周：论文修订，同行评议，最终完善

* 第 51-52 周：论文提交准备，项目总结

### 6.2 各阶段里程碑与交付物

**第一阶段里程碑**：



* 里程碑 1（第 5 周）：完成 Lean Mathlib 核心模块数据提取

* 里程碑 2（第 8 周）：建立基础数据清洗和解析流程

* 里程碑 3（第 11 周）：构建完整的定义依赖图谱

* 里程碑 4（第 13 周）：完成性质标签体系设计，产出 1000 + 标注样本

**交付物**：



* 数据提取报告（包含数据规模、质量评估）

* 清洗后的定义数据集（CSV 格式，10000 + 条目）

* 定义依赖图谱（GraphML 格式）

* 性质标签体系文档（含标注指南）

**第二阶段里程碑**：



* 里程碑 5（第 16 周）：完成双曲 GNN 基准模型实现

* 里程碑 6（第 19 周）：建立嵌入学习和性质预测框架

* 里程碑 7（第 22 周）：实现多任务学习和注意力机制

* 里程碑 8（第 25 周）：模型初步训练，达到基线性能

* 里程碑 9（第 29 周）：完成模型优化，性能评估报告

**交付物**：



* 双曲 GNN 模型代码（PyTorch 实现）

* 训练好的嵌入模型（支持性质预测）

* 性能评估报告（包含准确率、召回率等指标）

* 模型架构设计文档

**第三阶段里程碑**：



* 里程碑 10（第 32 周）：完成双曲空间几何分析

* 里程碑 11（第 35 周）：建立聚类分析和相似性度量方法

* 里程碑 12（第 38 周）：完成显式特征维度设计

* 里程碑 13（第 41 周）：完成案例研究，形成分析报告

* 里程碑 14（第 42 周）：完成中期评估，确定后续方向

**交付物**：



* 几何分析报告（包含线性可分性验证结果）

* 聚类分析和相似性研究报告

* 显式特征维度设计文档

* 案例研究报告（重点关注欧拉常数等）

**第四阶段里程碑**：



* 里程碑 15（第 45 周）：完成所有实验数据整理

* 里程碑 16（第 48 周）：完成论文初稿撰写

* 里程碑 17（第 50 周）：完成论文修订和完善

* 里程碑 18（第 52 周）：准备论文提交材料

**交付物**：



* 完整的研究论文（含实验数据和分析）

* 代码和数据的开源发布准备

* 项目总结报告

* 未来研究方向建议

### 6.3 风险评估与应对策略

**技术风险**：



1. **数据质量风险**：Lean Mathlib 数据可能存在不一致性或错误

* 应对策略：建立多层次数据验证机制，交叉检查

1. **模型性能风险**：双曲 GNN 可能无法达到预期性能

* 应对策略：设计多种模型架构，进行对比实验

1. **理论验证风险**：数学性质在双曲空间中的线性可分性假设可能不成立

* 应对策略：设计严格的统计检验，准备替代方案

**进度风险**：



1. **数据处理复杂度超预期**：Lean 语法复杂性可能导致数据处理时间延长

* 应对策略：分阶段处理，优先核心模块，并行处理

1. **模型训练时间风险**：大规模图数据训练可能需要更长时间

* 应对策略：使用 GPU 加速，优化算法，分批训练

1. **技术难题风险**：遇到无法解决的技术问题

* 应对策略：预留缓冲时间，寻求专家支持，调整研究计划

**资源风险**：



1. **计算资源风险**：GPU 资源不足影响模型训练

* 应对策略：提前申请计算资源，使用云服务，优化代码效率

1. **人力资源风险**：团队成员变动或专业技能不足

* 应对策略：建立知识共享机制，外部专家咨询，技能培训

**应对策略总结**：



* 建立每周进度检查机制，及时发现和解决问题

* 准备技术备选方案，避免单点故障

* 预留 20% 的缓冲时间应对意外情况

* 建立完善的文档记录，确保知识传承

* 保持与导师和同行的定期交流，获得及时支持

## 7. 总结与展望

### 7.1 研究成果预期

基于本研究的理论框架和实验设计，我们预期将取得以下主要成果：

**理论贡献**：



1. 建立数学对象在双曲空间中的几何表示理论，证明代数 / 拓扑性质的线性可分性

2. 提出基于双曲空间的 "层级爆炸" 问题解决方案，为大规模数学知识表示提供新方法

3. 设计 "显式特征维度" 分析框架，提高数学性质预测的可解释性

**技术创新**：



1. 开发高效的双曲图神经网络架构，专门用于数学知识图谱的性质预测

2. 建立大规模、高质量的数学性质标注数据集，推动该领域的发展

3. 实现数学概念的语义分析工具，支持未知对象性质的快速推断

**应用价值**：



1. 为数学教育提供智能化辅助工具，帮助学生理解数学概念关系

2. 为数学研究提供自动化分析手段，加速新定理的发现和证明

3. 为人工智能系统提供数学推理能力，支持科学计算和工程应用

### 7.2 未来研究方向

**近期研究方向（1-2 年）**：



1. **扩展到更多数学领域**：将方法推广到代数几何、微分方程、概率论等领域

2. **增强在线学习能力**：开发能够实时学习新数学概念的在线算法

3. **改进可解释性**：深化显式特征维度分析，提供更精确的语义解释

4. **集成大语言模型**：结合 LLM 技术，增强数学文本理解和推理能力

**中期研究方向（3-5 年）**：



1. **跨语言数学知识整合**：整合不同语言的数学资源，构建多语言数学知识图谱

2. **自动化定理发现**：基于双曲嵌入的相似性分析，自动发现新的数学关系

3. **交互式定理证明助手**：开发智能助手，辅助数学家进行复杂证明

4. **数学知识问答系统**：构建能够回答复杂数学问题的智能系统

**长期愿景（5 年以上）**：



1. **数学知识的统一表示**：建立覆盖所有数学领域的统一双曲空间表示框架

2. **数学直觉的机器模拟**：通过几何分析模拟数学家的直觉思维过程

3. **数学研究的自动化**：实现从问题提出到定理证明的全自动化过程

4. **数学教育革命**：基于 AI 技术的个性化数学教育，大幅提升学习效率

### 7.3 研究建议

**对研究者的建议**：



1. **扎实的数学基础**：深入理解双曲几何和数学知识表示理论

2. **跨学科合作**：加强与数学家、逻辑学家、教育专家的合作

3. **持续创新**：在现有方法基础上不断探索新的技术路径

4. **开源共享**：及时分享研究成果和代码，推动领域发展

**对项目管理的建议**：



1. **分阶段实施**：按照本报告的路线图逐步推进，确保每个阶段的质量

2. **风险管控**：建立完善的风险评估和应对机制

3. **团队建设**：组建跨学科团队，确保具备所需的专业技能

4. **资源配置**：合理配置计算资源和人力资源，提高效率

**对未来发展的建议**：



1. **标准化建设**：推动数学知识表示和性质标注的标准化

2. **工具生态**：构建完整的工具链，降低研究门槛

3. **应用推广**：积极探索在教育、科研、产业中的应用场景

4. **国际合作**：加强国际交流，参与全球数学 AI 发展

本研究通过将双曲几何与数学知识表示相结合，为解决数学性质预测这一挑战性问题提供了创新的解决方案。随着研究的深入和技术的不断进步，我们相信这一方向将为数学 AI 领域带来重要突破，推动数学知识的智能化处理和应用达到新的高度。

**参考资料&#x20;**

\[1] Hyperbolic Graph Convolutional Neural Networks(pdf)[ https://cs.stanford.edu/\~jure/pubs/hgcn-neurips19.pdf](https://cs.stanford.edu/~jure/pubs/hgcn-neurips19.pdf)

\[2] Hyperbolic-PDE GNN: Spectral Graph Neural Networks in the Perspective of A System of Hyperbolic Partial Differential Equations[ https://arxiv.org/html/2505.23014v1/](https://arxiv.org/html/2505.23014v1/)

\[3] LGIN: Defining an Approximately Powerful Hyperbolic GNN(pdf)[ https://arxiv.org/pdf/2504.00142v3](https://arxiv.org/pdf/2504.00142v3)

\[4] Node-Specific Space Selection via Localized Geometric Hyperbolicity in Graph Neural Networks(pdf)[ https://object.cloud.sdsc.edu/v1/AUTH\_da4962d3368042ac8337e2dfdd3e7bf3/ml-papers/TMLR/2024/nodespecific\_space\_selection\_via\_localized\_geometric\_hyperbolicity\_in\_graph\_neural\_networks\_\_f2061013.pdf](https://object.cloud.sdsc.edu/v1/AUTH_da4962d3368042ac8337e2dfdd3e7bf3/ml-papers/TMLR/2024/nodespecific_space_selection_via_localized_geometric_hyperbolicity_in_graph_neural_networks__f2061013.pdf)

\[5] HYPERBOLIC GRAPH NEURAL NETWORKS: A REVIEW OF METHODS AND APPLICATIONS(pdf)[ https://scispace.com/pdf/hyperbolic-graph-neural-networks-a-review-of-methods-and-2fkhxgf5.pdf](https://scispace.com/pdf/hyperbolic-graph-neural-networks-a-review-of-methods-and-2fkhxgf5.pdf)

\[6] Hyperbolic multi-channel hypergraph convolutional neural network based on multilayer hypergraph(pdf)[ https://pmc.ncbi.nlm.nih.gov/articles/PMC12241348/pdf/41598\_2025\_Article\_8594.pdf](https://pmc.ncbi.nlm.nih.gov/articles/PMC12241348/pdf/41598_2025_Article_8594.pdf)

\[7] Hyperbolic Graph Neural Networks-CSDN博客[ https://blog.csdn.net/weixin\_40248634/article/details/103834800](https://blog.csdn.net/weixin_40248634/article/details/103834800)

\[8] 基于双曲空间的高效图卷积网络框架:an end-to-end hyperbolic deep graph convolutional neural network framework 实战解析-CSDN博客[ https://blog.csdn.net/2600\_94960131/article/details/157313885](https://blog.csdn.net/2600_94960131/article/details/157313885)

\[9] 激活函数：神经网络的灵魂与非线性转换核心[ https://www.iesdouyin.com/share/video/7573610352550645011/?region=\&mid=7572507329543867142\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=GW96qWj.OrrK1OTayZoYelxNwT5KvmOKlg2yk9mW75I-\&share\_version=280700\&ts=1774022995\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7573610352550645011/?region=\&mid=7572507329543867142\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=GW96qWj.OrrK1OTayZoYelxNwT5KvmOKlg2yk9mW75I-\&share_version=280700\&ts=1774022995\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[10] Hyperbolic Graph Neural Networks: A Review of Methods and Applications(pdf)[ https://arxiv.org/pdf/2202.13852v4](https://arxiv.org/pdf/2202.13852v4)

\[11] 模型训练方法、电子设备和计算机可读存储介质[ https://www.xjishu.com/zhuanli/55/202411801834.html](https://www.xjishu.com/zhuanli/55/202411801834.html)

\[12] Low-Dimensional Hyperbolic Knowledge Graph Embeddings[ https://arxiv.org/pdf/2005.00545](https://arxiv.org/pdf/2005.00545)

\[13] Multi-hop Knowledge Graph Reasoning Based on Hyperbolic Knowledge Graph Embedding and Reinforcement Learning[ https://dl.acm.org/doi/fullHtml/10.1145/3502223.3502224](https://dl.acm.org/doi/fullHtml/10.1145/3502223.3502224)

\[14] Designing Hierarchies for Optimal Hyperbolic Embedding(pdf)[ http://melika.xyz/data/eswc\_paper.pdf?trk=public\_post\_comment-text](http://melika.xyz/data/eswc_paper.pdf?trk=public_post_comment-text)

\[15] Hyperbolic Hierarchical Knowledge Graph Embeddings for Link Prediction in Low Dimensions[ https://arxiv.org/pdf/2204.13704v1](https://arxiv.org/pdf/2204.13704v1)

\[16] Knowledge graph representation via hierarchical hyperbolic neural graph embedding[ https://www.amazon.science/publications/knowledge-graph-representation-via-hierarchical-hyperbolic-neural-graph-embedding](https://www.amazon.science/publications/knowledge-graph-representation-via-hierarchical-hyperbolic-neural-graph-embedding)

\[17] Hyperbolic Knowledge Graph Embeddings for Knowledge Base Completion[ https://pmc.ncbi.nlm.nih.gov/articles/PMC7250606/pdf/978-3-030-49461-2\_Chapter\_12.pdf](https://pmc.ncbi.nlm.nih.gov/articles/PMC7250606/pdf/978-3-030-49461-2_Chapter_12.pdf)

\[18] Bending the Future: Autoregressive Modeling of Temporal Knowledge Graphs in Curvature-Variable Hyperbolic Spaces(pdf)[ https://arxivhtbprolorg-s.evpn.library.nenu.edu.cn/pdf/2209.05635](https://arxivhtbprolorg-s.evpn.library.nenu.edu.cn/pdf/2209.05635)

\[19] Graph Contrastive Pre-training for Effective Theorem Reasoning(pdf)[ https://arxiv.org/pdf/2108.10821v1](https://arxiv.org/pdf/2108.10821v1)

\[20] Graph Representations for Higher-Order Logic and Theorem Proving[ https://research.google/pubs/graph-representations-for-higher-order-logic-and-theorem-proving/](https://research.google/pubs/graph-representations-for-higher-order-logic-and-theorem-proving/)

\[21] Nazrin: Atomic Tactics for Graph Neural Networks for Theorem Proving in Lean 4[ https://arxiv.org/html/2602.18767v2](https://arxiv.org/html/2602.18767v2)

\[22] GraphMind: Theorem Selection and Conclusion Generation Framework with Dynamic GNN for LLM Reasoning[ https://chatpaper.com/zh-CN/chatpaper/paper/212560](https://chatpaper.com/zh-CN/chatpaper/paper/212560)

\[23] GraphMind: Theorem Selection and Conclusion Generation Framework with Dynamic GNN for LLM Reasoning(pdf)[ https://www.arxiv.org/pdf/2511.19078](https://www.arxiv.org/pdf/2511.19078)

\[24] A Simple Proof of the Universality of[ https://www.arxiv-vanity.com/papers/1910.03802/](https://www.arxiv-vanity.com/papers/1910.03802/)

\[25] Graph2Tac: Online Representation Learning of Formal Math Concepts[ https://research.ibm.com/publications/graph2tac-online-representation-learning-of-formal-math-concepts](https://research.ibm.com/publications/graph2tac-online-representation-learning-of-formal-math-concepts)

\[26] Nazrin: Atomic Tactics for Graph Neural Networks for Theorem Proving in Lean 4[ https://arxiv.org/html/2602.18767v1/](https://arxiv.org/html/2602.18767v1/)

\[27] Combining Textual and Structural Information for Premise Selection in Lean[ https://arxiv.org/html/2510.23637v1](https://arxiv.org/html/2510.23637v1)

\[28] Lean4trace: Data augmentation for neural theorem proving in Lean[ https://openreview.net/pdf/7bc6e168a9fe100095a13b5221a503d8d173f3ab.pdf](https://openreview.net/pdf/7bc6e168a9fe100095a13b5221a503d8d173f3ab.pdf)

\[29] Alchemy: Amplifying Theorem-Proving Capability through Symbolic Mutation[ https://arxiv.org/html/2410.15748](https://arxiv.org/html/2410.15748)

\[30] Basic properties of holors[ https://leanprover-community.github.io/mathlib\_docs/data/holor](https://leanprover-community.github.io/mathlib_docs/data/holor)

\[31] Formalization of Neural Networks in Lean 4[ https://github.com/or4nge19/NeuralNetworks](https://github.com/or4nge19/NeuralNetworks)

\[32] Beyond Euclidian Embeddings (Introduction to Hyperbolic Embeddings)(pdf)[ https://www.cs.columbia.edu/\~verma/classes/uml/slides/uml\_L10\_hyperbolic\_embeddings.pdf](https://www.cs.columbia.edu/~verma/classes/uml/slides/uml_L10_hyperbolic_embeddings.pdf)

\[33] Representation Tradeoffs for Hyperbolic Embeddings[ https://pmc.ncbi.nlm.nih.gov/articles/PMC6534139/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6534139/)

\[34] 双曲几何入门指南:Poincaré圆盘模型的6个关键直觉与层次嵌入设计原理 - CSDN文库[ https://wenku.csdn.net/column/5643c9f63j](https://wenku.csdn.net/column/5643c9f63j)

\[35] HYPERBOLIC LARGE LANGUAGE MODELS[ https://arxiv.org/pdf/2509.05757](https://arxiv.org/pdf/2509.05757)

\[36] The hyperbolic geometry of financial networks - PMC[ https://pmc.ncbi.nlm.nih.gov/articles/PMC7910495/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7910495/)

\[37] A GROUP-THEORETIC FRAMEWORK FOR MACHINE LEARNING IN HYPERBOLIC SPACES[ https://arxiv.org/pdf/2501.06934v1.pdf](https://arxiv.org/pdf/2501.06934v1.pdf)

\[38] Hypergraph Applications In Ai And Geometry[ https://www.restack.io/p/hypergraph-applications-in-ai-answer-hyperbolic-geometry-machine-learning-cat-ai](https://www.restack.io/p/hypergraph-applications-in-ai-answer-hyperbolic-geometry-machine-learning-cat-ai)

\[39] Nested Hyperbolic Spaces for Context-Aware LLM Reasoning: A Geometric Framework[ https://www.techrxiv.org/users/1024367/articles/1384203/master/file/data/nested\_hyperbolic\_spaces/nested\_hyperbolic\_spaces.pdf](https://www.techrxiv.org/users/1024367/articles/1384203/master/file/data/nested_hyperbolic_spaces/nested_hyperbolic_spaces.pdf)

\[40] Multiarc and curve graphs are hierarchically hyperbolic[ https://arxiv.org/html/2311.04356v2/](https://arxiv.org/html/2311.04356v2/)

\[41] New tools in hierarchical hyperbolicity: A survey[ https://arxiv.org/html/2507.17546v1/](https://arxiv.org/html/2507.17546v1/)

\[42] A Combinatorial Structure for Many Hierarchically Hyperbolic Spaces(pdf)[ https://research-information.bris.ac.uk/files/377107465/2308.16335v1.pdf](https://research-information.bris.ac.uk/files/377107465/2308.16335v1.pdf)

\[43] Exponential Functions 1[ http://tasks.illustrativemathematics.org/blueprints/M1/5](http://tasks.illustrativemathematics.org/blueprints/M1/5)

\[44] Orders of Growth[ http://mlwiki.org/index.php/Orders\_of\_Growth](http://mlwiki.org/index.php/Orders_of_Growth)

\[45] Khan Academy | Khan Academy[ https://es.khanacademy.org/standards/CCSS.Math/HSF.LE](https://es.khanacademy.org/standards/CCSS.Math/HSF.LE)

\[46] 程序员的数学(七)指数爆炸:如何应对 “越算越庞大” 的编程难题-CSDN博客[ https://blog.csdn.net/2301\_76297596/article/details/155642974](https://blog.csdn.net/2301_76297596/article/details/155642974)

\[47] 13.1: Exponential Functions[ https://math.libretexts.org/Courses/Cosumnes\_River\_College/Math\_375:\_Pre-Calculus/13:\_Exponential\_and\_Logarithmic\_Functions/13.01:\_Exponential\_Functions](https://math.libretexts.org/Courses/Cosumnes_River_College/Math_375:_Pre-Calculus/13:_Exponential_and_Logarithmic_Functions/13.01:_Exponential_Functions)

\[48] Exponential Growth and Decay[ https://mathresearch.utsa.edu/wiki/index.php?title=Exponential\_Growth\_and\_Decay](https://mathresearch.utsa.edu/wiki/index.php?title=Exponential_Growth_and_Decay)

\[49] What is… hierarchical hyperbolicity?[ https://arxiv.org/html/2601.15410v1/](https://arxiv.org/html/2601.15410v1/)

\[50] 理解双曲空间中的数据表示:为何它能颠覆传统层次建模(仅1%人知晓的几何优势) - CSDN文库[ https://wenku.csdn.net/column/4kjkno7mde](https://wenku.csdn.net/column/4kjkno7mde)

\[51] Story of Hyperbolicity: a journey from geometry to solvability of word problems in non-technical terms[ https://www.cheenta.com/story-of-hyperbolicity-a-journey-from-geometry-to-solvability-of-word-problems-in-non-technical-terms/page/5/](https://www.cheenta.com/story-of-hyperbolicity-a-journey-from-geometry-to-solvability-of-word-problems-in-non-technical-terms/page/5/)

\[52] Nested Hyperbolic Spaces for Dimensionality Reduction and Hyperbolic NN Design[ https://pmc.ncbi.nlm.nih.gov/articles/PMC9997089/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9997089/)

\[53] Feature-aware ultra-low dimensional reduction of real networks[ https://arxiv.org/html/2401.09368](https://arxiv.org/html/2401.09368)

\[54] Hydra: A method for strain-minimizing hyperbolic embedding of network- and distance-based data[ https://www.arxiv-vanity.com/papers/1903.08977/](https://www.arxiv-vanity.com/papers/1903.08977/)

\[55] An improved hyperbolic embedding algorithm[ https://academic.oup.com/comnet/article/6/3/321/4727184](https://academic.oup.com/comnet/article/6/3/321/4727184)

\[56] Do We Need Curved Spaces? A Critical Look at Hyperbolic Graph Learning in Graph Classification[ https://mlg-europe.github.io/2025/papers/cameraReady/274/CameraReady/HGCN\_MLG2025\_final.pdf](https://mlg-europe.github.io/2025/papers/cameraReady/274/CameraReady/HGCN_MLG2025_final.pdf)

\[57] Representation Tradeoffs for Hyperbolic Embeddings - PubMed[ https://pubmed.ncbi.nlm.nih.gov/31131375/](https://pubmed.ncbi.nlm.nih.gov/31131375/)

\[58] Embedding Text in Hyperbolic Spaces(pdf)[ https://preview.aclanthology.org/nschneid-metadata-dialog/W18-1708.pdf](https://preview.aclanthology.org/nschneid-metadata-dialog/W18-1708.pdf)

\[59] 大模型 到底 是 啥 ？ 8 分钟 速 通 ！ 大模型 到底 是 啥 ？ 8 分钟 速 通 ！[ https://www.iesdouyin.com/share/video/7514545758977264896/?region=\&mid=7514546521593940774\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=lsf96IYFYMIaBgaa0EtimkqXfwyHr08Xqc1LolEZEOU-\&share\_version=280700\&ts=1774023051\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7514545758977264896/?region=\&mid=7514546521593940774\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=lsf96IYFYMIaBgaa0EtimkqXfwyHr08Xqc1LolEZEOU-\&share_version=280700\&ts=1774023051\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[60] Representation Tradeoffs for Hyperbolic Embeddings[ https://pmc.ncbi.nlm.nih.gov/articles/PMC6534139/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6534139/)

\[61] GraphRAG的“降维打击”!HyperbolicRAG登场，用“双曲几何”重构层次推理，性能飙升!-CSDN博客[ https://blog.csdn.net/m0\_59163425/article/details/155313339](https://blog.csdn.net/m0_59163425/article/details/155313339)

\[62] hyperbolic space[ https://www.britannica.com/science/hyperbolic-space](https://www.britannica.com/science/hyperbolic-space)

\[63] 双曲空间上等距群离散性剖析与相关问题探究.docx-原创力文档[ https://m.book118.com/html/2026/0304/8024133051010050.shtm](https://m.book118.com/html/2026/0304/8024133051010050.shtm)

\[64] Adaptive data embedding for curved spaces - PMC[ https://pmc.ncbi.nlm.nih.gov/articles/PMC11625262/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11625262/)

\[65] A Set-to-Set Distance Measure in Hyperbolic Space[ https://arxiv.org/html/2506.18529v1](https://arxiv.org/html/2506.18529v1)

\[66] Geodesics in Hyperbolic Space[ https://www.fiveable.me/key-terms/non-euclidean-geometry/geodesics-in-hyperbolic-space](https://www.fiveable.me/key-terms/non-euclidean-geometry/geodesics-in-hyperbolic-space)

\[67] UHCone: Universal Hyperbolic Cone For Implicit Hierarchical Learning[ https://openreview.net/pdf?id=BBgop7vYvX](https://openreview.net/pdf?id=BBgop7vYvX)

\[68] The Role of Entropy in Guiding a Connection Prover[ https://arxiv.org/pdf/2105.14706](https://arxiv.org/pdf/2105.14706)

\[69] Low-Dimensional Hyperbolic Knowledge Graph Embeddings[ https://aclanthology.org/anthology-files/anthology-files/anthology-files/pdf/acl/2020.acl-main.617.pdf](https://aclanthology.org/anthology-files/anthology-files/anthology-files/pdf/acl/2020.acl-main.617.pdf)

\[70] Combining Textual and Structural Information for Premise Selection in Lean[ https://arxiv.org/pdf/2510.23637](https://arxiv.org/pdf/2510.23637)

\[71] Bounded combinatorics and uniform models for hyperbolic 3-manifolds[ https://arxiv.org/pdf/1312.2293](https://arxiv.org/pdf/1312.2293)

\[72] Nazrin: Atomic Tactics for Graph Neural Networks for Theorem Proving in Lean 4[ https://arxiv.org/pdf/2602.18767](https://arxiv.org/pdf/2602.18767)

\[73] GENERALIZATIONS OF THE KOLMOGOROV–BARZDIN EMBEDDING ESTIMATES[ https://arxiv.org/pdf/1103.3423](https://arxiv.org/pdf/1103.3423)

\[74] Continuous-Discrete Message Passing for Graph Logic Reasoning[ http://typo3.p514932.webspaceconfig.de/fileadmin/user\_upload/Continuous-Discrete\_Message\_Passing\_for\_Graph\_Logic\_Reasoning.pdf](http://typo3.p514932.webspaceconfig.de/fileadmin/user_upload/Continuous-Discrete_Message_Passing_for_Graph_Logic_Reasoning.pdf)

\[75] Modeling Heterogeneous Hierarchies with Relation-specific Hyperbolic Cones[ https://proceedings.neurips.cc/paper\_files/paper/2021/file/662a2e96162905620397b19c9d249781-Paper.pdf](https://proceedings.neurips.cc/paper_files/paper/2021/file/662a2e96162905620397b19c9d249781-Paper.pdf)

\[76] Learning Symbolic Physics with Graph Networks[ https://arxiv.org/pdf/1909.05862](https://arxiv.org/pdf/1909.05862)

\[77] Integrating graph neural networks into cvc5[ https://aitp-conference.org/2024/abstract/AITP\_2024\_paper\_8.pdf](https://aitp-conference.org/2024/abstract/AITP_2024_paper_8.pdf)

\[78] Hyperbolic embeddability of locally complete almost complex submanifolds[ http://www.numdam.org/item/10.1016/j.crma.2011.01.020.pdf](http://www.numdam.org/item/10.1016/j.crma.2011.01.020.pdf)

\[79] HAKG: Hierarchy-Aware Knowledge Gated Network for Recommendation[ https://arxiv.org/pdf/2204.04959](https://arxiv.org/pdf/2204.04959)

\[80] GRAPH2TAC: LEARNING HIERARCHICAL REPRESENTATIONS OF MATH CONCEPTS IN THEOREM PROVING[ https://openreview.net/pdf?id=XyB4VvF01X](https://openreview.net/pdf?id=XyB4VvF01X)

\[81] Hierarchical Symbolic Reasoning in Hyperbolic Space for Deep Discriminative Models[ https://arxiv.org/pdf/2207.01916](https://arxiv.org/pdf/2207.01916)

\[82] Formalized Hopfield Networks and Boltzmann Machines[ https://arxiv.org/pdf/2512.07766](https://arxiv.org/pdf/2512.07766)

\[83] Security check required[ https://www.researchgate.net/publication/395540703\_Sharp\_Sobolev\_and\_Adams-Trudinger-Moser\_inequalities\_for\_symmetric\_functions\_without\_boundary\_conditions\_on\_hyperbolic\_spaces\_Sharp\_Sobolev\_and\_Adams-Trudinger-MoserJ\_M\_do\_O\_et\_al](https://www.researchgate.net/publication/395540703_Sharp_Sobolev_and_Adams-Trudinger-Moser_inequalities_for_symmetric_functions_without_boundary_conditions_on_hyperbolic_spaces_Sharp_Sobolev_and_Adams-Trudinger-MoserJ_M_do_O_et_al)

\[84] Knowledge Association with Hyperbolic Knowledge Graph Embeddings[ https://aclanthology.org/2020.emnlp-main.460.pdf](https://aclanthology.org/2020.emnlp-main.460.pdf)

\[85] HyperMR: Hyperbolic Hypergraph Multi-hop Reasoning for Knowledge-based Visual Question Answering[ https://aclanthology.org/2024.lrec-main.746.pdf](https://aclanthology.org/2024.lrec-main.746.pdf)

\[86] TORCHLEAN: Formalizing Neural Networks in Lean[ https://arxiv.org/pdf/2602.22631](https://arxiv.org/pdf/2602.22631)

\[87] Nazrin: Atomic Tactics for Graph Neural Networks for Theorem Proving in Lean 4[ https://arxiv.org/html/2602.18767v1/](https://arxiv.org/html/2602.18767v1/)

\[88] Formalization of Neural Networks in Lean 4[ https://github.com/or4nge19/NeuralNetworks](https://github.com/or4nge19/NeuralNetworks)

\[89] Basic properties of holors[ https://leanprover-community.github.io/mathlib\_docs/data/holor](https://leanprover-community.github.io/mathlib_docs/data/holor)

\[90] ProofNet++: A Neuro-Symbolic System for Formal Proof Verification with Self-Correction[ https://openreview.net/pdf/33eb9eb3fde185d4839606d10a084509039e631b.pdf](https://openreview.net/pdf/33eb9eb3fde185d4839606d10a084509039e631b.pdf)

\[91] Math Behind Neural Networks[ https://learn.codesignal.com/preview/lessons/768?ref=mentorcruise](https://learn.codesignal.com/preview/lessons/768?ref=mentorcruise)

\[92] A Logic for Reasoning About Aggregate-Combine Graph Neural Networks(pdf)[ https://arxiv.org/pdf/2405.00205v1](https://arxiv.org/pdf/2405.00205v1)

\[93] GraphMR: Graph Neural Network for Mathematical Reasoning(pdf)[ https://preview.aclanthology.org/nschneid-metadata-dialog/2021.emnlp-main.273.pdf](https://preview.aclanthology.org/nschneid-metadata-dialog/2021.emnlp-main.273.pdf)

\[94] Decidability of Graph Neural Networks via Logical Characterizations(pdf)[ https://arxiv.org/pdf/2404.18151](https://arxiv.org/pdf/2404.18151)

\[95] 南瓜书pumpkin-book图神经网络:GNN公式推导解析-CSDN博客[ https://blog.csdn.net/gitblog\_00773/article/details/151140112](https://blog.csdn.net/gitblog_00773/article/details/151140112)

\[96] Graph Neural Networks[ https://snap-stanford.github.io/cs224w-notes/machine-learning-with-networks/graph-neural-networks](https://snap-stanford.github.io/cs224w-notes/machine-learning-with-networks/graph-neural-networks)

\[97] What is a GNN (graph neural network)?[ https://www.ibm.com/think/topics/graph-neural-network](https://www.ibm.com/think/topics/graph-neural-network)

\[98] Generating Millions Of Lean Theorems With Proofs By Exploring State Transition Graphs(pdf)[ https://www.arxiv.org/pdf/2503.04772](https://www.arxiv.org/pdf/2503.04772)

\[99] Mathlib介绍 - CSDN文库[ https://wenku.csdn.net/answer/67zwb963jg](https://wenku.csdn.net/answer/67zwb963jg)

\[100] LeanConjecturer: Automatic Generation of Mathematical Conjectures for Theorem Proving(pdf)[ http://121.43.168.64:10060/s/org/arxiv/G.https/pdf/2506.22005?;x-chain-id=b739r7v256v4](http://121.43.168.64:10060/s/org/arxiv/G.https/pdf/2506.22005?;x-chain-id=b739r7v256v4)

\[101] LeanProgress: Guiding Search for Neural Theorem Proving via Proof Progress Prediction[ https://arxiv.org/pdf/2502.17925v3](https://arxiv.org/pdf/2502.17925v3)

\[102] PROOF ARTIFACT CO-TRAINING FOR THEOREM PROVING WITH LANGUAGE MODELS[ https://mathai-iclr.github.io/papers/papers/MATHAI\_23\_paper.pdf?utm\_campaign=The%20Batch\&utm\_medium=email&\_hsmi=152811001&\_hsenc=p2ANqtz-\_LGI8t74DqPz9W0rAv4KpiJXiadiw0VPPu2n1V0GcXHVDD0bgrM4l6DJalvwvOpVUv4vIP02pnW3Dcg4fgQbsG4\_4rWw\&utm\_content=152811001\&utm\_source=hs\_email](https://mathai-iclr.github.io/papers/papers/MATHAI_23_paper.pdf?utm_campaign=The%20Batch\&utm_medium=email&_hsmi=152811001&_hsenc=p2ANqtz-_LGI8t74DqPz9W0rAv4KpiJXiadiw0VPPu2n1V0GcXHVDD0bgrM4l6DJalvwvOpVUv4vIP02pnW3Dcg4fgQbsG4_4rWw\&utm_content=152811001\&utm_source=hs_email)

\[103] Lean4trace: Data augmentation for neural theorem proving in Lean[ https://openreview.net/notes/edits/attachment?id=Q8qKgR94AI\&name=pdf](https://openreview.net/notes/edits/attachment?id=Q8qKgR94AI\&name=pdf)

\[104] LeanProgress: Guiding Search for Neural Theorem Proving via Proof Progress Prediction[ https://leandojo.org/leanprogress.html](https://leandojo.org/leanprogress.html)

\[105] GitHub - kim-em/lean-training-data[ https://github.com/kim-em/lean-training-data](https://github.com/kim-em/lean-training-data)

\[106] Structured data extraction and programmatic interaction with Lean 4.[ https://github.com/Kripner/leantree](https://github.com/Kripner/leantree)

\[107] axle-mcp[ https://github.com/Vilin97/axle-mcp/blob/main/README.md](https://github.com/Vilin97/axle-mcp/blob/main/README.md)

\[108] User Guide — LeanDojo 4.20.0 documentation[ https://leandojo.readthedocs.io/en/latest/user-guide.html](https://leandojo.readthedocs.io/en/latest/user-guide.html)

\[109] Lemmas about Array.extract[ https://leanprover-community.github.io/mathlib4\_docs/Mathlib/Data/Array/Extract.html](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Data/Array/Extract.html)

\[110] chore: use authenticated gh api in nightly bump workflow #341[ https://github.com/leanprover/cslib/pull/341/files/0c37e3be4ff7d4739881ec3ee52ada0686a44572](https://github.com/leanprover/cslib/pull/341/files/0c37e3be4ff7d4739881ec3ee52ada0686a44572)

\[111] 探索LeanDojo:机器学习在定理证明中的革命-CSDN博客[ https://blog.csdn.net/gitblog\_00567/article/details/141443535](https://blog.csdn.net/gitblog_00567/article/details/141443535)

\[112] Standard Constructions for Graphs[ https://www.math.uzh.ch/sepp/magma-2.17\_10-cr/html/text1636.htm](https://www.math.uzh.ch/sepp/magma-2.17_10-cr/html/text1636.htm)

\[113] CHAPTER 11 Construction of Graphs(pdf)[ https://moscow.sci-hub.st/4531/2dfcf5b9093a77b3d87c6e850029830a/construction-of-graphs.pdf#navpanes=0\&view=FitH](https://moscow.sci-hub.st/4531/2dfcf5b9093a77b3d87c6e850029830a/construction-of-graphs.pdf#navpanes=0\&view=FitH)

\[114] Degree-based graph construction(pdf)[ https://arxiv.org/pdf/0905.4892](https://arxiv.org/pdf/0905.4892)

\[115] Standard Constructions for Graphs[ https://www.math.ru.nl/magma/text618.html](https://www.math.ru.nl/magma/text618.html)

\[116] Construction of Graphs and Digraphs[ https://www.math.ru.nl/magma/text615.html](https://www.math.ru.nl/magma/text615.html)

\[117] Math 3322: Graph Theory Lecture 7: Regular graphs(pdf)[ https://facultyweb.kennesaw.edu/mlavrov/courses/graph-theory/lecture7.pdf#:\~:text=numbers,](https://facultyweb.kennesaw.edu/mlavrov/courses/graph-theory/lecture7.pdf#:~:text=numbers,)

\[118] PROOFLOW: A DEPENDENCY GRAPH APPROACH TO FAITHFUL PROOF AUTOFORMALIZATION(pdf)[ https://arxiv.org/pdf/2510.15981](https://arxiv.org/pdf/2510.15981)

\[119] KnowTeX: Visualizing Mathematical Dependencies[ https://arxiv.org/html/2601.15294v1](https://arxiv.org/html/2601.15294v1)

\[120] Text-Based DFS Coq Dependency Analyzer[ https://github.com/noya2012/Text-Based-DFS-Coq-Dependency-Analyzer/blob/main/README.md](https://github.com/noya2012/Text-Based-DFS-Coq-Dependency-Analyzer/blob/main/README.md)

\[121] Lean Graph[ https://github.com/patrik-cihal/lean-graph](https://github.com/patrik-cihal/lean-graph)

\[122] GitHub - coq-community/coq-dpdgraph: Build dependency graphs between Coq objects \[maintainers=@Karmaki,@ybertot][ https://github.com/coq-community/coq-dpdgraph/](https://github.com/coq-community/coq-dpdgraph/)

\[123] GitHub - holdenlee/depgraph: Draw dependency graphs for math theorems[ https://github.com/holdenlee/depgraph](https://github.com/holdenlee/depgraph)

\[124] TheoremDep源码解析:基于静态站点生成器的定理依赖关系追踪系统 - CSDN文库[ https://wenku.csdn.net/doc/479q7d33c8](https://wenku.csdn.net/doc/479q7d33c8)

\[125] 图论基本知识-CSDN博客[ https://blog.csdn.net/Mitsui14wung/article/details/118618959](https://blog.csdn.net/Mitsui14wung/article/details/118618959)

\[126] Discrete Mathematics in Computer Science C1. Introduction to Graphs(pdf)[ https://ai.dmi.unibas.ch/\_files/teaching/hs22/dmics/slides/dmics-c01-handout4.pdf](https://ai.dmi.unibas.ch/_files/teaching/hs22/dmics/slides/dmics-c01-handout4.pdf)

\[127] Unveiling Graph Structures in Microservices: Service Dependency Graph, Call Graph, and Causal Graph(pdf)[ https://www.abhishek-tiwari.com/pdf/unveiling-graph-structures-in-microservices-service-dependency-graph-call-graph-and-causal-graph.pdf](https://www.abhishek-tiwari.com/pdf/unveiling-graph-structures-in-microservices-service-dependency-graph-call-graph-and-causal-graph.pdf)

\[128] 4 Graph Theory\nThe power and (pdf)[ https://oa.ee.tsinghua.edu.cn/\~ouzhijian/pgm/pgm-pdf/CDLS\_chapter4-5.pdf](https://oa.ee.tsinghua.edu.cn/~ouzhijian/pgm/pgm-pdf/CDLS_chapter4-5.pdf)

\[129] Not All Features Deserve Attention: Graph-Guided Dependency Learning for Tabular Data Generation with Language Models(pdf)[ https://preview.aclanthology.org/scil-homepage/2025.findings-emnlp.330.pdf](https://preview.aclanthology.org/scil-homepage/2025.findings-emnlp.330.pdf)

\[130] Edge‐featured graph attention network with dependency features for causality detection of events[ https://www.researchgate.net/publication/370652838\_Edge-featured\_graph\_attention\_network\_with\_dependency\_features\_for\_causality\_detection\_of\_events](https://www.researchgate.net/publication/370652838_Edge-featured_graph_attention_network_with_dependency_features_for_causality_detection_of_events)

\[131] Lean Graph[ https://github.com/patrik-cihal/lean-graph](https://github.com/patrik-cihal/lean-graph)

\[132] Graph centrality analysis of feature dependencies to unveil modeling intents(pdf)[ https://cad-journal.net/files/vol\_15/CAD\_15(5)\_2018\_684-696.pdf](https://cad-journal.net/files/vol_15/CAD_15\(5\)_2018_684-696.pdf)

\[133] Bag-of-Vector Embeddings of Dependency Graphs for Semantic Induction[ https://www.virascience.com/document/79df2e429b24c33a365703f0f7b0b44bf2c62fea/](https://www.virascience.com/document/79df2e429b24c33a365703f0f7b0b44bf2c62fea/)

\[134] Graph Theory Part One[ https://www.stanford.edu/class/cs103/lectures/08/Lecture%20Slides.pdf](https://www.stanford.edu/class/cs103/lectures/08/Lecture%20Slides.pdf)

\[135] What are Graphs and How to Use Them[ https://www.luisllamas.es/en/what-is-a-graph/](https://www.luisllamas.es/en/what-is-a-graph/)

\[136] Graph Theory[ https://omniscient.wiki/article/graph\_theory](https://omniscient.wiki/article/graph_theory)

\[137] Graph Models[ https://graph.build/resources/graph-models](https://graph.build/resources/graph-models)

\[138] Euler–Mascheroni constant[ https://en-academic.com/dic.nsf/enwiki/102308/29977](https://en-academic.com/dic.nsf/enwiki/102308/29977)

\[139] Euler–Mascheroni constant[ https://oeis.org/wiki/Continued\_fraction\_expansion\_of\_Euler%E2%80%93Mascheroni\_constant](https://oeis.org/wiki/Continued_fraction_expansion_of_Euler%E2%80%93Mascheroni_constant)

\[140] EulerGamma[ https://reference.wolfram.com/language/ref/EulerGamma](https://reference.wolfram.com/language/ref/EulerGamma)

\[141] mathlib4/Mathlib/NumberTheory/Harmonic/EulerMascheroni.lean at master · leanprover-community/mathlib4 · GitHub[ https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/NumberTheory/Harmonic/EulerMascheroni.lean](https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/NumberTheory/Harmonic/EulerMascheroni.lean)

\[142] 欧拉常数\[莱昂哈德·欧拉提出的数学常数]\_百科[ https://m.baike.com/wiki/%E6%AC%A7%E6%8B%89%E5%B8%B8%E6%95%B0/503070?baike\_source=doubao](https://m.baike.com/wiki/%E6%AC%A7%E6%8B%89%E5%B8%B8%E6%95%B0/503070?baike_source=doubao)

\[143] 欧拉-马歇罗尼常数\_欧拉马歇罗尼常数100位-CSDN博客[ https://blog.csdn.net/likunyuan0830/article/details/152420205](https://blog.csdn.net/likunyuan0830/article/details/152420205)

\[144] 欧拉 常数 的 存在 性 证明 。 # 数学 # 每日 一 题 # 考研 # 竞赛 # 每天 学习 一点点[ https://www.iesdouyin.com/share/note/7599280295879249202/?region=\&mid=7579965261327960859\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&schema\_type=37\&share\_sign=zRCie7uB1V3Y1jzPGFN1ySuFuFNF2f24JNjM04pitaU-\&share\_version=280700\&ts=1774023093\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/note/7599280295879249202/?region=\&mid=7579965261327960859\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&schema_type=37\&share_sign=zRCie7uB1V3Y1jzPGFN1ySuFuFNF2f24JNjM04pitaU-\&share_version=280700\&ts=1774023093\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[145] The Euler constant : γ(pdf)[ https://scipp.ucsc.edu/\~haber/archives/physics116A10/euler.pdf](https://scipp.ucsc.edu/~haber/archives/physics116A10/euler.pdf)

\[146] Euler-Mascheroni Constant[ https://brilliant.org/wiki/euler-mascheroni-constant/](https://brilliant.org/wiki/euler-mascheroni-constant/)

\[147] EULER'S CONSTANT(pdf)[ https://web.mae.ufl.edu/uhk/EULER-CONSTANT.pdf](https://web.mae.ufl.edu/uhk/EULER-CONSTANT.pdf)

\[148] Collection of formulae for Euler’s constant γ(pdf)[ https://scipp-legacy.pbsci.ucsc.edu/\~haber/archives/physics116A11/euler2.pdf](https://scipp-legacy.pbsci.ucsc.edu/~haber/archives/physics116A11/euler2.pdf)

\[149] Integral Representations[ https://web.mit.edu/axiom-math\_v8.14/arch/amd64\_linux26/mnt/doc/dlmfintegralrepresentations.xhtml](https://web.mit.edu/axiom-math_v8.14/arch/amd64_linux26/mnt/doc/dlmfintegralrepresentations.xhtml)

\[150] Constante d'Euler-Mascheroni[ https://wikimonde.com/article/Constante\_d%27Euler-Mascheroni](https://wikimonde.com/article/Constante_d%27Euler-Mascheroni)

\[151] Euler's constant[ https://fungrim.org/topic/Euler%27s\_constant.html](https://fungrim.org/topic/Euler%27s_constant.html)

\[152] An Infinite Product for \\(e^{\gamma}\\) via Hypergeometric Formulas for Euler's Constant γ[ https://archive.org/download/arXiv\_pdf\_0306\_002/arXiv\_pdf\_0306\_002.tar/0306/math0306008.pdf](https://archive.org/download/arXiv_pdf_0306_002/arXiv_pdf_0306_002.tar/0306/math0306008.pdf)

\[153] A Unifying Integral Representation of the Gamma Function and Its Reciprocal\*(pdf)[ https://web3.arxiv.org/pdf/2506.12112](https://web3.arxiv.org/pdf/2506.12112)

\[154] COMPLEX ANALYSIS: LECTURE 32(pdf)[ https://people.math.osu.edu/gautam.42/S20/LectureNotes/Lecture32.pdf](https://people.math.osu.edu/gautam.42/S20/LectureNotes/Lecture32.pdf)

\[155] 【γ14】オイラー定数の積分表示２選・調和数・積分評価（ガンマ関数の基礎14）[ https://mamekebi-science.com/math/spetialfunction/gamma14/](https://mamekebi-science.com/math/spetialfunction/gamma14/)

\[156] Constante d'Euler-Mascheroni[ https://wikimonde.com/article/Constante\_d%27Euler-Mascheroni](https://wikimonde.com/article/Constante_d%27Euler-Mascheroni)

\[157] Euler–Mascheroni constant[ https://oeis.org/wiki/Continued\_fraction\_expansion\_of\_Euler%E2%80%93Mascheroni\_constant](https://oeis.org/wiki/Continued_fraction_expansion_of_Euler%E2%80%93Mascheroni_constant)

\[158] EULER'S INTEGRALS[ https://www.phys.uconn.edu/\~rozman/Courses/P2400\_24S/downloads/eulers-integral.pdf](https://www.phys.uconn.edu/~rozman/Courses/P2400_24S/downloads/eulers-integral.pdf)

\[159] EULER'S CONSTANT[ https://web.mae.ufl.edu/uhk/EULER-CONSTANT.pdf](https://web.mae.ufl.edu/uhk/EULER-CONSTANT.pdf)

\[160] Harmonic Series And Its Parts[ https://www.cut-the-knot.org/arithmetic/algebra/HarmonicSeries.shtml](https://www.cut-the-knot.org/arithmetic/algebra/HarmonicSeries.shtml)

\[161] 6+∞ new expressions for the Euler-Mascheroni constant[ https://arxiv.org/pdf/1904.09855v1.pdf](https://arxiv.org/pdf/1904.09855v1.pdf)

\[162] Euler–Mascheroni Constant :  History[ https://www.encyclopedia.pub/entry/history/show/84731](https://www.encyclopedia.pub/entry/history/show/84731)

\[163] EULER-MASCHERONI CONSTANT[ https://web.mae.ufl.edu/uhk/EULER-MASCHERONI.pdf](https://web.mae.ufl.edu/uhk/EULER-MASCHERONI.pdf)

\[164] Milestones for Research Degrees (Mathematics)[ https://www.imperial.ac.uk/mathematics/postgraduate/doctoral-programme/current-students/milestones/](https://www.imperial.ac.uk/mathematics/postgraduate/doctoral-programme/current-students/milestones/)

\[165] Theses and Major Research Projects[ https://students.wlu.ca/programs/science/mathematics/graduate-students/theses-and-major-research-projects.html](https://students.wlu.ca/programs/science/mathematics/graduate-students/theses-and-major-research-projects.html)

\[166] Stage 3[ https://lsa.umich.edu/math/graduates/GraduateStudentHandbook/ph-d-programs1/ph-d--program-requirements/stage-3.html](https://lsa.umich.edu/math/graduates/GraduateStudentHandbook/ph-d-programs1/ph-d--program-requirements/stage-3.html)

\[167] 课题研究时间线模板与任务分配指南[ https://www.iesdouyin.com/share/note/7528813026313522492/?region=\&mid=7518614759257590565\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&schema\_type=37\&share\_sign=C6dUyCINcdU18h2TuJwRZNWYsHGq8t2aXNk.emS8L38-\&share\_version=280700\&ts=1774023117\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/note/7528813026313522492/?region=\&mid=7518614759257590565\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&schema_type=37\&share_sign=C6dUyCINcdU18h2TuJwRZNWYsHGq8t2aXNk.emS8L38-\&share_version=280700\&ts=1774023117\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[168] Thesis Process[ https://mcs.stanford.edu/academics/thesis-process](https://mcs.stanford.edu/academics/thesis-process)

\[169] Sample Timeline[ https://www.colorado.edu/math/graduate/current-students/sample-timeline](https://www.colorado.edu/math/graduate/current-students/sample-timeline)

\[170] The Thesis Timeline[ https://ecampusontario.pressbooks.pub/craftingresearchnarratives/front-matter/the-thesis-timeline/](https://ecampusontario.pressbooks.pub/craftingresearchnarratives/front-matter/the-thesis-timeline/)

\[171] MLR-Copilot: Autonomous Machine Learning Research based on Large Language Models Agents(pdf)[ https://arxiv.org/pdf/2408.14033](https://arxiv.org/pdf/2408.14033)

\[172] Three-pillar Evidence-based Methodological Framework for Experimental Machine Learning Studies(pdf)[ https://www.techrxiv.org/users/886160/articles/1296613/master/file/data/Three\_pillar\_Evidence\_based\_Methodological\_Framework\_for\_Experimental\_Machine\_Learning\_Studies-2/Three\_pillar\_Evidence\_based\_Methodological\_Framework\_for\_Experimental\_Machine\_Learning\_Studies-2.pdf](https://www.techrxiv.org/users/886160/articles/1296613/master/file/data/Three_pillar_Evidence_based_Methodological_Framework_for_Experimental_Machine_Learning_Studies-2/Three_pillar_Evidence_based_Methodological_Framework_for_Experimental_Machine_Learning_Studies-2.pdf)

\[173] AIMS: An Automatic Semantic Machine Learning Microservice Framework to Support Biomedical and Bioengineering Research(pdf)[ https://mdpi-res.com/d\_attachment/bioengineering/bioengineering-10-01134/article\_deploy/bioengineering-10-01134-v3.pdf?version=1696645080](https://mdpi-res.com/d_attachment/bioengineering/bioengineering-10-01134/article_deploy/bioengineering-10-01134-v3.pdf?version=1696645080)

\[174] Using AI to Find Evidence-Based Actions to Achieve Modelable Goals[ https://techtransfer.universityofcalifornia.edu/NCD/34373.html](https://techtransfer.universityofcalifornia.edu/NCD/34373.html)

\[175] AMD and Johns Hopkins Researchers Develop AI Agent Framework to Automate Scientific Research Process[ https://www.infoq.com/news/2025/01/amd-jhu-ai-lab-research-agent/](https://www.infoq.com/news/2025/01/amd-jhu-ai-lab-research-agent/)

\[176] Free for students, educators, and academic researchers.  Always.[ https://wandb.ai/site/research](https://wandb.ai/site/research)

\[177] REVES: REasoning in VErification and Security[ https://gtr.ukri.org/projects?ref=EP/K032674/1](https://gtr.ukri.org/projects?ref=EP/K032674/1)

\[178] PhysProver:推动物理自动定理证明-腾讯云开发者社区-腾讯云[ https://cloud.tencent.com/developer/article/2636990?policyId=1003](https://cloud.tencent.com/developer/article/2636990?policyId=1003)

\[179] 课题标书撰写的核心结构与立项成功关键[ https://www.iesdouyin.com/share/note/7511522749353970985/?region=\&mid=6782384489638135810\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&schema\_type=37\&share\_sign=zvghyKFUb6RGydoAmnvm0QoEkTGkQmcsUQBf8IMZRLc-\&share\_version=280700\&ts=1774023117\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/note/7511522749353970985/?region=\&mid=6782384489638135810\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&schema_type=37\&share_sign=zvghyKFUb6RGydoAmnvm0QoEkTGkQmcsUQBf8IMZRLc-\&share_version=280700\&ts=1774023117\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[180] 陶哲轩宣布“等式理论计划”成功，57天完成2200万+数学关系证明\_量子位[ http://m.toutiao.com/group/7440316701108863538/?upstream\_biz=doubao](http://m.toutiao.com/group/7440316701108863538/?upstream_biz=doubao)

\[181] 15-815 Automated Theorem Proving

Projects[ https://www.cs.cmu.edu/\~fp/courses/atp/projects.html](https://www.cs.cmu.edu/~fp/courses/atp/projects.html)

\[182] 结合非形式化推理递归构建形式化证明-腾讯云开发者社区-腾讯云[ https://cloud.tencent.cn/developer/article/2637335](https://cloud.tencent.cn/developer/article/2637335)

> （注：文档部分内容可能由 AI 生成）