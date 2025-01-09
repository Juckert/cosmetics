const imageUploadField = document.getElementById('upload-file');
const capturePhotoButton = document.getElementById('capture-photo');
const buttonClosingImageEdition = document.querySelector('.button-text');
const imagePreview = document.getElementById('preview-image');
const imgUploadOverlay = document.querySelector('.img-upload__overlay');
const clearButton = document.querySelector('.button-2 .button-text');
const form = document.getElementById('upload-form');
const results = document.querySelector('.hint-text');
const scaleSmallerButton = document.querySelector('.scale__control--smaller');
const scaleBiggerButton = document.querySelector('.scale__control--bigger');
const scaleValueInput = document.querySelector('.scale__control--value');
const checkButton = document.getElementById('check-button');

let scale = 100;

// Обработчик события загрузки файла
imageUploadField.addEventListener('change', (evt) => {
  const file = evt.target.files[0];
  if (file) {
      const reader = new FileReader();
      reader.onload = () => {
          imagePreview.src = reader.result;
          imgUploadOverlay.classList.remove('hidden');
          document.querySelector('.img-upload__scale').classList.remove('hidden');
      };
      reader.onerror = (e) => {
          console.error('Error reading file:', e);
      };
      reader.readAsDataURL(file);
  }
});

// Очистка формы
const clearForm = () => {
  imgUploadOverlay.classList.add('hidden');
  imageUploadField.value = '';
  scale = 100;
  scaleValueInput.value = `${scale}%`;
  imagePreview.style.transform = `scale(1)`;
};

// Обработчик события закрытия редактирования изображения
buttonClosingImageEdition.addEventListener('click', () => {
  clearForm();
  console.log('закрыли редактор изображения');
});

// Обработчик события очистки выбора
clearButton.addEventListener('click', () => {
  clearForm();
  console.log('очистили форму');
});

// Обработчик события уменьшения масштаба
scaleSmallerButton.addEventListener('click', () => {
  if (scale > 100) {
      scale -= 10;
      scaleValueInput.value = `${scale}%`;
      imagePreview.style.transform = `scale(${scale / 100})`;
  }
});

// Обработчик события увеличения масштаба
scaleBiggerButton.addEventListener('click', () => {
  if (scale < 200) {
      scale += 10;
      scaleValueInput.value = `${scale}%`;
      imagePreview.style.transform = `scale(${scale / 100})`;
  }
});

// Обработчик события отправки формы
form.addEventListener('submit', (evt) => {
  evt.preventDefault();
  const file = imageUploadField.files[0]; // загруженный файл
  if (file) {
      const canvas = document.createElement('canvas'); // создаем эл-т canvas для работы с изобр
      const ctx = canvas.getContext('2d'); // контекст рисования для канвас
      const img = new Image(); // новый объект имаге
      img.src = imagePreview.src; // путь к изображению из предварительного просмотра
      img.onload = () => { // обработчик события, когда изображение загрузится
          const originalWidth = img.width; // параметры изображения
          const originalHeight = img.height;
          const newWidth = originalWidth * (scale / 100);
          const newHeight = originalHeight * (scale / 100);
          const x = (originalWidth - newWidth) / 2; // координаты для центрирования
          const y = (originalHeight - newHeight) / 2;

          canvas.width = newWidth; // устанавливаем параметры канвас
          canvas.height = newHeight;
          ctx.drawImage(img, x, y, newWidth, newHeight, 0, 0, newWidth, newHeight); // рисуем изображение на канвас
          // конвертируем канвас в блоб в формате
          canvas.toBlob((blob) => {
              // код для отправки данных на сервер (в комментах чтобы не мешался, ибо сервера еще нет, надо доделать)
              /*
              const formData = new FormData();
              formData.append('file', blob, file.name);

              const serverUrl = '/upload'; // Здесь будет адрес сервера

              fetch(serverUrl, {
                  method: 'POST',
                  body: formData
              })
              .then(response => response.json())
              .then(data => {
                  const resultsDiv = results;
                  resultsDiv.innerHTML = '<p>' + data.message + '</p>';
              })
              .catch(error => {
                  console.error('Error:', error);
              });
              */

              // Попап с адресом изображения и информацией об обрезке (проверка, что все работает норм)
              const cropPercentage = ((originalWidth - newWidth) / originalWidth * 100).toFixed(2);
              alert(`Изображение загружено\nОригинальные размеры: ${originalWidth}x${originalHeight}\nНовые размеры: ${newWidth}x${newHeight}\nОбрезано на: ${cropPercentage}%\nПуть: ${imagePreview.src}`);

              // Временная заглушка для отображения результата из текстового файла
              // Я хотела сделать так, но fetch не может быть выполнено из-за того, что пока нет сервера (политика безопасности CORS ограничивает запросы к локальным файлам)
              /*fetch('./output.txt')
              .then(response => response.text())
              .then(data => {
                  const resultsDiv = results;
                  resultsDiv.innerHTML = '<p>' + data + '</p>';
              })*/
              // отображаем это после отправки формы (заглушка, убрать потом)
              const output = "Все круто";
              results.classList.add('hint-text-black'); //делаем текст черным
              results.textContent = output;

          }, 'image/jpeg'); // 'image/jpeg' - это формат изображения, в котором будет создан BLOB (Binary Large Object)
          clearForm();
      };
  }
});

// Обработчик события захвата фото с камеры (с ноута работает, с телефона не дает проверить без защищенного подключения)
capturePhotoButton.addEventListener('click', () => {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
          .then((mediaStream) => {
              const video = document.createElement('video');
              video.srcObject = mediaStream;
              video.play();

              const canvas = document.createElement('canvas');
              const ctx = canvas.getContext('2d');

              video.onloadedmetadata = () => {
                  canvas.width = video.videoWidth;
                  canvas.height = video.videoHeight;
                  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                  canvas.toBlob((blob) => {
                      const file = new File([blob], 'captured_image.jpg', { type: 'image/jpeg' });
                      const dataTransfer = new DataTransfer();
                      dataTransfer.items.add(file);
                      imageUploadField.files = dataTransfer.files;

                      const evt = new Event('change', { bubbles: true });
                      imageUploadField.dispatchEvent(evt);

                      mediaStream.getTracks().forEach(track => track.stop());
                  }, 'image/jpeg');
              };
          })
          .catch((error) => {
              console.error('Error accessing the camera:', error);
              if (error.name === 'NotAllowedError') {
                  alert('Доступ к камере запрещен. Пожалуйста, проверьте настройки разрешений в вашем браузере.');
              } else if (error.name === 'NotFoundError') {
                  alert('Камера не найдена. Пожалуйста, убедитесь, что у вас есть доступная камера.');
              } else {
                  alert('Произошла ошибка при доступе к камере. Пожалуйста, попробуйте снова.');
              }
          });
  } else {
      console.error('getUserMedia is not supported by your browser');
      alert('Ваш браузер не поддерживает доступ к камере.');
  }
});
