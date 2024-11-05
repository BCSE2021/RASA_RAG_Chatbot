import re
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain

class OutputParser(StrOutputParser):
    def __init__(self) -> None:
        super().__init__()

    def parse(self, text:str) -> str:
        return self.extract_answer(text)

    def extract_answer(self, text_response: str, pattern: str = r"Answer:\s*(.*)") -> str:
        match = re.search(pattern, text_response, re.DOTALL)
        if match:
            answer_text = match.group(1).strip()
            return answer_text
        else: 
            return text_response
        
class Offilne_RAG:  
    def __init__(self, llm) -> None:
        self.llm = llm
        self.prompt = hub.pull("rlm/rag-prompt")
        self.str_parser = OutputParser()
        self.template = """Bạn là một chatbot trợ lý chương trình được thiết kế để hỗ trợ trả lời câu hỏi của sinh viên tại Đại học Việt Nhật. Mục tiêu của bạn là cung cấp các phản hồi chính xác và hữu ích. Nếu một sinh viên đặt câu hỏi và bạn biết câu trả lời, hãy trả lời bằng thông tin rõ ràng và súc tích. Nếu không có câu trả lời, hãy nói Tôi không biết.
                           \nQuestion: {question} 
                           \nContext: {context} 
                           \nAnswer:"""
        self.prompt_decompos = PromptTemplate.from_template(self.template)
    def get_chain(self,retriever):
        input_data ={
            "context": retriever | self.format_docs,
            "question": RunnablePassthrough()
        }
        rag_chain = (
            input_data
            | self.prompt_decompos
            | self.llm
            | self.str_parser
        )
        print(self.prompt)
        return rag_chain
    
    def format_docs(self,docs):
        return "\n\n".join(doc.page_content for doc in docs)

# class Offilne_RAG:  
#     def __init__(self, llm) -> None:
#         self.llm = llm
#         self.prompt = hub.pull("rlm/rag-prompt")
#         self.str_parser = OutputParser()
#         self.template = """Bạn là một chatbot trợ lý chương trình được thiết kế để hỗ trợ trả lời câu hỏi của sinh viên tại Đại học Việt Nhật. Mục tiêu của bạn là cung cấp các phản hồi chính xác và hữu ích. Nếu một sinh viên đặt câu hỏi và bạn biết câu trả lời, hãy trả lời bằng thông tin rõ ràng và súc tích. Nếu bạn không chắc chắn hoặc không có đủ thông tin để trả lời câu hỏi, chỉ cần nói 'Tôi xin lỗi, tôi không biết câu trả lời cho câu hỏi đó.' Không cung cấp bất kỳ thông tin không chính xác hoặc ngẫu nhiên nào
#                            Question: {question} 
#                            Context: {context} 
#                            Answer:"""
#         self.prompt_decompos = PromptTemplate.from_template(self.template)

#         self.contextualize_q_system_prompt = """Với lịch sử trò chuyện và câu hỏi mới nhất của người dùng \
#         có thể tham chiếu đến ngữ cảnh trong lịch sử trò chuyện, hãy xây dựng một câu hỏi độc lập \
#         có thể hiểu được mà không cần lịch sử trò chuyện. KHÔNG trả lời câu hỏi, \
#         chỉ cần xây dựng lại câu hỏi nếu cần và nếu không thì trả lại câu hỏi nguyên trạng."""
#         self.contextualize_q_prompt = ChatPromptTemplate.from_messages(
#             [
#                 ("system", self.contextualize_q_system_prompt),
#                 MessagesPlaceholder(variable_name="chat_history"),
#                 ("human", "{question}"),
#             ])
#         self.contextualize_q_chain = self.contextualize_q_prompt | self.llm | StrOutputParser()


#     def contextualized_question (self,input:dict):
#         if input.get("chat_history"):
#             new_question = self.contextualize_q_chain.invoke(input)
#             print(f"Câu hỏi đã chỉnh sửa: {new_question}")
#             return new_question
#         else:
#             return input["question"]

#     def get_chain(self,retriever):
#         input_data ={
#             "context": retriever | self.format_docs,
#             "question": RunnablePassthrough()
#         }
#         retriever_chain = RunnablePassthrough.assign(context = self.contextualize_q_chain | retriever | self.format_docs
#                                                      )

#         rag_chain = (
#             retriever_chain
#             | self.prompt_decompos
#             | self.llm
#             | self.str_parser 
#         )
#         return rag_chain
    
#     def format_docs(self,docs):
#         return "\n\n".join(doc.page_content for doc in docs)
    


# class Offilne_RAG:  
#     def __init__(self, llm) -> None:
#         self.llm = llm
#         self.prompt = hub.pull("rlm/rag-prompt")
#         self.str_parser = OutputParser()
#         self.template = """Bạn là một chatbot trợ lý chương trình được thiết kế để hỗ trợ trả lời câu hỏi của sinh viên tại Đại học Việt Nhật. Mục tiêu của bạn là cung cấp các phản hồi chính xác và hữu ích. Nếu một sinh viên đặt câu hỏi và bạn biết câu trả lời, hãy trả lời bằng thông tin rõ ràng và súc tích. Nếu bạn không chắc chắn hoặc không có đủ thông tin để trả lời câu hỏi, chỉ cần nói 'Tôi xin lỗi, tôi không biết câu trả lời cho câu hỏi đó.' Không cung cấp bất kỳ thông tin không chính xác hoặc ngẫu nhiên nào
#                            Question: {input} 
#                            Context: {context} 
#                            Answer:"""
#         self.prompt_decompos = PromptTemplate.from_template(self.template)

#         self.qaprompt = ChatPromptTemplate.from_messages([
#             ("system", self.template),
#             MessagesPlaceholder(variable_name="chat_history"),
#             ("human", "{input}"),
#         ])

#         self.contextualize_q_system_prompt = """Với lịch sử trò chuyện và câu hỏi mới nhất của người dùng \
#         có thể tham chiếu đến ngữ cảnh trong lịch sử trò chuyện, hãy xây dựng một câu hỏi độc lập \
#         có thể hiểu được mà không cần lịch sử trò chuyện. KHÔNG trả lời câu hỏi, \
#         chỉ cần xây dựng lại câu hỏi nếu cần và nếu không thì trả lại câu hỏi nguyên trạng."""

#         self.contextualize_q_prompt = ChatPromptTemplate.from_messages(
#             [
#                 ("system", self.contextualize_q_system_prompt),
#                 MessagesPlaceholder(variable_name="chat_history"),
#                 ("human", "{input}"),
#             ])
#         self.contextualize_q_chain = self.contextualize_q_prompt | self.llm | StrOutputParser()
#         self.store ={}

#     def get_session_history(self, session_id:str):
#         if session_id not in self.store:
#             self.store[session_id] = ChatMessageHistory()
#         return self.store[session_id]

#     def get_chain(self,retriever):
#         history_aware_retriever = create_history_aware_retriever(self.llm, retriever, self.contextualize_q_prompt)
#         retriever_chain = RunnablePassthrough.assign(context = self.contextualize_q_chain | retriever | self.format_docs)
#         question_answer_chain = create_stuff_documents_chain(self.llm, self.qaprompt)
#         rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
#         # rag_chain = (
#         #     retriever_chain
#         #     | self.prompt_decompos
#         #     | self.llm
#         #     | self.str_parser 
#         # )

#         with_message_history = RunnableWithMessageHistory(
#             rag_chain,
#             self.get_session_history,
#             input_messages_key="question",
#             history_messages_key="chat_history",
#             output_messages_key="answer"
#         )
#         return with_message_history
    
#     def format_docs(self,docs):
#         return "\n\n".join(doc.page_content for doc in docs)
    


