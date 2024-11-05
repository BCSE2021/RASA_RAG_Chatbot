import torch
print(torch.cuda.is_available())  # Trả về True nếu GPU được nhận diện
print(torch.cuda.get_device_name(0))