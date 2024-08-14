document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('button[id^="previewButton-"]').forEach(button => {
    button.addEventListener('click', function () {
      const postId = this.id.split('-')[1];
      const form = this.closest('form');
      const previewContent = document.getElementById(`previewContent-${postId}`);

      const formData = new FormData(form);
      const text = formData.get('text');
      const username = formData.get('username') || 'Anonymous';

      const now = new Date();
      const dateFormatted = `${String(now.getDate()).padStart(2, '0')}.${String(now.getMonth() + 1).padStart(2, '0')}.${now.getFullYear()} в ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

      const avatarFile = formData.get('avatar');
      const avatarURL = avatarFile && avatarFile instanceof File
        ? URL.createObjectURL(avatarFile)
        : '';

      if (avatarFile && avatarFile instanceof File) {
        setTimeout(() => URL.revokeObjectURL(avatarURL), 10000);
      }

      previewContent.innerHTML = `
        <div style="background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; margin-bottom: 15px; max-width: 600px; word-wrap: break-word;">
            <div style="background-color: #f5f6f8; display: flex; align-items: center; padding: 10px;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #ccc; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                    ${avatarFile && avatarFile instanceof File
                        ? `<img src="${avatarURL}" alt="${username}'s avatar" style="width: 40px; height: 40px; border-radius: 50%;" />`
                        : '<span style="font-size: 20px; color: #fff;">?</span>'}
                </div>
                <div>
                    <strong style="font-weight: bold; margin-right: 10px;">${username}</strong>
                    <span style="font-weight: lighter; line-height: 1; font-size: 0.8rem; margin: 0; padding: 0; color: #6c757d;">${dateFormatted}</span>
                </div>
            </div>
            <p style="margin-top: 10px; margin-bottom: 0; overflow-wrap: break-word;">${text}</p>
        </div>
      `;
    });
  });
});
