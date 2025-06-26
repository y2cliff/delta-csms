<script nonce="csms_custom_script">
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[id^='follow-button-']").forEach(function(button) {
        button.addEventListener("click", function () {
            let icon = button.querySelector("i");
            let objectId = button.getAttribute("data-object-id");
            let app_name = button.getAttribute("data-app-name");
            let model_name = button.getAttribute("data-model-name");

            fetch(`/toggle-follow/${app_name}/${model_name}/${objectId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_following) {
                    button.textContent = " Unfollow";
                    icon.className = "bi bi-person-dash-fill";
                } else {
                    button.textContent = " Follow";
                    icon.className = "bi bi-person-plus-fill";
                }
                button.prepend(icon);
            });
        });
    });
});
</script>
