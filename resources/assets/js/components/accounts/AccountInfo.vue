<template>
  <div class="col w-full md:w-5/12">
    <div class="row">
      <div class="col w-full sm:w-5/12">
        <div class="flex flex-wrap">
          <div class="flex mb-auto mt-2 mr-2">
            <img
              src="../../../../assets/image/icons/calendar-category.svg"
              alt=""
            />
          </div>

          <div
            @click="changeSelectedAccount(accountPayload)"
            v-if="account_is_enabled"
          >
            <router-link
              class="font-semibold text-2xl"
              :to="{ path: '/user/budgetcommander/' + this.account_id }"
            >
              <span class="font-semibold text-2xl" v-html="accountNameHtml" />
            </router-link>
          </div>

          <div @click="displayAccountDisabledAlert" v-if="!account_is_enabled">
            <a
              class="font-semibold text-2xl cursor-not-allowed"
              :disabled="!account_is_enabled"
            >
              <span class="font-semibold text-2xl" v-html="accountNameHtml">
              </span>
            </a>
          </div>
        </div>
      </div>

      <div class="col w-full sm:w-7/12 flex flex-wrap">
        <div class="w-full sm:w-1/2 px-2">
          <label class="block mb-5" for="username"
            >SPEND ({{ spend | currency(account_currency_symbol) }})</label
          >
          <div class="bg-background w-full rounded h-6">
            <div
              class=" rounded"
              :class="[parseInt(budgetWidth) > 99 ? 'bg-danger' : 'bg-success']"
              :style="{ width: budgetWidth }"
            >
              &nbsp;
            </div>
          </div>
        </div>

        <div class="w-full sm:w-1/2 px-2">
          <label
            class="block mb-5"
            for="username"
            v-if="kpi_name.toUpperCase() == 'ROAS'"
            >ROAS ({{ kpi_value }})</label
          >
          <label class="block mb-5" for="username" v-else
            >CPA ({{ kpi_value | currency(account_currency_symbol) }})</label
          >
          <div class="bg-background w-full rounded h-6">
            <div
              class=" rounded"
              :class="[parseInt(kpiWidth) > 99 ? 'bg-danger' : 'bg-success']"
              :style="{ width: kpiWidth }"
            >
              &nbsp;
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "AccountInfo",
  props: {
    name: {
      type: String,
      required: true,
    },
    account_id: {
      type: String,
      required: true,
    },
    spend: {
      type: Number,
      required: true,
    },
    kpi_target_value: {
      type: Number,
      required: true,
    },
    kpi_name: {
      type: String,
      required: true,
    },
    budget: {
      type: Number,
      required: true,
    },
    rollover_spend: {
      type: [Number, Boolean],
      required: false,
    },
    excess_budget: {
      type: Number,
      required: false,
    },
    kpi_value: {
      type: Number,
      required: true,
    },
    account_currency_code: {
      type: String,
      required: true,
    },
    account_currency_symbol: {
      type: String,
      required: true,
    },
    account_name: {
      type: String,
      required: true,
    },
    account_timezone: {
      type: String,
      required: true,
    },
    account_google_id: {
      type: String,
      required: true,
    },
    account_is_enabled: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {};
  },
  computed: {
    accountNameHtml() {
      let name = "";
      let words = this.name.split(" ");
      if (words.length < 3) {
        name = "<p>" + this.name + "</p><p>&nbsp;</p>";
      } else {
        name = "<p>";
        name += words.splice(0, 2).join(" ");
        name += "</p><p>";
        name += words.join(" ");
        name += "</p>";
      }
      return name;
    },
    budgetWidth() {
      let budget =
        this.rollover_spend && this.excess_budget > 0
          ? this.budget + this.excess_budget
          : this.budget;
      let vs =
        this.spend / budget > 1 ? 100 : Number(this.spend / budget) * 100;
      return vs + "%";
    },
    kpiWidth() {
      let vs =
        this.kpi_value / this.kpi_target_value > 1
          ? 100
          : Number(this.kpi_value / this.kpi_target_value) * 100;
      return vs + "%";
    },
    accountPayload() {
      return {
        account_currency_code: this.account_currency_code,
        account_currency_symbol: this.account_currency_symbol,
        account_id: this.account_id,
        account_name: this.account_name,
        account_timezone: this.account_timezone,
        account_google_id: this.account_google_id,
      };
    },
  },
  methods: {
    ...mapActions(["changeSelectedAccount", "createAlert"]),
    displayAccountDisabledAlert() {
      this.createAlert({
        headline: "Inactive Account",
        message: "This account hasn't been synced yet",
        dismissSecs: 5,
      });
    },
  },
  mounted() {},
};
</script>

<style scoped></style>
