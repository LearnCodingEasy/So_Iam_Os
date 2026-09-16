
<template>
  <div class="wrapper_page_login">
    <div class="inner_page_login">
      <div class="container mx-auto">
        <div class="wrapper_content_page_login">
          <div
            class="inner_content_page_login w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12"
          >
            <div
              class="box_content_page_login mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_6 desktop_item_6 desktop_lg_item_6"
            >
              <div class="mobile_body_dark">
                <span class="voice_up"> </span>
                <span class="voice_down"> </span>
                <span class="power"> </span>
                <span class="sonser"> </span>
                <span class="voice"> </span>
                <span class="carme"> </span>
                <div class="mobile_content">
                  <LoginForm />
                </div>
              </div>
            </div>
            <div
              class="box_content_page_login mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_6 desktop_item_6 desktop_lg_item_6"
            >
              <div class="mobile_body_dark">
                <span class="voice_up"> </span>
                <span class="voice_down"> </span>
                <span class="power"> </span>
                <span class="sonser"> </span>
                <span class="voice"> </span>
                <span class="carme"> </span>
                <div class="mobile_content">
                  <SignupForm />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LoginForm from '@/components/Authentication/LoginForm.vue'
import SignupForm from '@/components/Authentication/SignupForm.vue'

export default {
  name: 'AuthPage',
  components: { LoginForm, SignupForm },
}
</script>
