<template>
  <div class="flex">
    <sidemenu :user_id="user_id" />

    <headermenu :user_id="user_id" />

    <div class="flex bg-gray-200 w-full h-full">
      <router-view></router-view>
    </div>

    <alerts />
  </div>
</template>

<script>
import axios from "axios";
import Sidemenu from "../components/common/SideMenu";
import Headermenu from "../components/common/HeaderMenu";
import Alerts from "../components/common/Alerts.vue";
import { mapActions } from "vuex";

export default {
  data: function() {
    return {
      user_id: ""
    };
  },
  methods: {
    ...mapActions(["changeSelectedUser", "changeSelectedAccount"]),
    updateUserId() {
      this.loading = false;

      if (typeof this.$route.params.user_id !== "undefined") {
        this.changeSelectedUser(this.$route.params.user_id);
        return
      }

      if (localStorage.getItem("user_id")) {
        this.changeSelectedUser(localStorage.getItem("user_id"));
        return
      }

      throw("Error assigning user id")

    }
  },

  created() {
    this.updateUserId()

    const selected_account_payload = {
      account_currency_code: localStorage.getItem("account_currency_code"),
      account_currency_symbol: localStorage.getItem("account_currency_symbol"),
      account_id: localStorage.getItem("account_id"),
      account_name: localStorage.getItem("account_name"),
      account_timezone: localStorage.getItem("account_timezone"),
      account_google_id: localStorage.getItem("account_google_id")
    };

    this.changeSelectedAccount(selected_account_payload);
  },
  components: {
    Alerts,
    Sidemenu,
    Headermenu
  }
};
</script>
<style scoped>
</style>