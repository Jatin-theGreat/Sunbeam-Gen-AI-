"""from langchain_text_splitters import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
docs = text_splitter.create_documents(["Artificial Intelligence (AI) is transforming the world at an unprecedented pace. From healthcare and education to finance and transportation, AI-driven systems are being integrated into nearly every domain of human activity. At its core, artificial intelligence refers to the ability of machines to perform tasks that typically require human intelligence. These tasks include learning from experience, recognizing patterns, understanding natural language, making decisions, and solving complex problems."])
print(docs)"""

row_texts =([ """Artificial Intelligence (AI) is transforming the world at an unprecedented pace. From healthcare and education to finance and transportation, AI-driven systems are being integrated into nearly every domain of human activity. At its core, artificial intelligence refers to the ability of machines to perform tasks that typically require human intelligence. These tasks include learning from experience, recognizing patterns, understanding natural language, making decisions, and solving complex problems.

Machine learning is a subfield of artificial intelligence that focuses on developing algorithms that allow computers to learn from data without being explicitly programmed. Instead of following predefined rules, machine learning models identify patterns in large datasets and use those patterns to make predictions or classifications. Supervised learning, unsupervised learning, and reinforcement learning are the three primary categories of machine learning techniques. Each of these approaches serves different purposes and is suitable for different types of problems.

Deep learning is a specialized branch of machine learning that uses neural networks with multiple layers, often referred to as deep neural networks. These models are inspired by the structure and function of the human brain. Deep learning has been particularly successful in areas such as image recognition, speech processing, natural language understanding, and autonomous systems. Convolutional Neural Networks (CNNs) are widely used for image-related tasks, while Recurrent Neural Networks (RNNs) and Transformers are commonly applied in sequence-based problems like language modeling.

Natural Language Processing (NLP) is a key application area of artificial intelligence that enables machines to understand, interpret, and generate human language. NLP techniques are used in chatbots, virtual assistants, sentiment analysis, machine translation, and information retrieval systems. Recent advancements in large language models have significantly improved the quality of text generation and comprehension, making human–computer interaction more natural and intuitive.

Despite its many benefits, artificial intelligence also raises ethical and social concerns. Issues such as data privacy, algorithmic bias, transparency, and job displacement have become important topics of discussion. Responsible AI development requires careful consideration of these challenges to ensure that technology is used in a fair, safe, and inclusive manner. Governments, researchers, and industry leaders are actively working to establish guidelines and regulations to govern the ethical use of AI.

As AI continues to evolve, it is expected to play an even greater role in shaping the future. Innovations in generative models, robotics, and human–AI collaboration will redefine how people work and live. Understanding the fundamentals of artificial intelligence is becoming increasingly important for students, professionals, and policymakers alike. By learning how AI systems function and how they are applied, individuals can better adapt to the rapidly changing technological landscape.
"""])
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap = 100, separators=["\n\n", "\n", " ", ""])
docs = text_splitter.create_documents(row_texts)
print(docs)
