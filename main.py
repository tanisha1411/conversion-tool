# from doc_analyzer import analyze_document

# file_path = 'sample_files/Invoice.pdf'  # Replace with your actual file
# user_query = "Summarize the important points in the document."

# structured_data, answer = analyze_document(file_path, user_query)

# print("\n--- STRUCTURED DATA ---")
# print(structured_data)

# print("\n--- QUERY RESPONSE ---")
# print(answer)


#Without API
from doc_analyzer import analyze_document

file_path = 'sample_files/merc.png'
user_query = input("Enter your query about the document: ")

structured_data, answer = analyze_document(file_path, user_query)

print("\n STRUCTURED DATA ")
print(structured_data)

print("\n--- ANSWER ---")
print(answer)
