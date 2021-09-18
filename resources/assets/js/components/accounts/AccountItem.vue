<template>
  <div 
  
    class="py-2"         
  >
    <div class="card row m-0 relative">
      <div
        @click="toggleShowStats"
        class="absolute right-0 top-0 p-4 cursor-pointer"
        v-if="accountIsEnabled"
      >
        <img
          class="cursor-pointer"
          src="../../../../assets/image/icons/restore.svg"
          alt=""
        />
      </div>

      <AccountInfo
        :name="account.name"
        :spend="getSpend"
        :kpi_target_value="kpi_target_value"
        :kpi_name="kpi"
        :budget="budget"
        :rollover_spend="rollover_spend"
        :excess_budget="excess_budget"
        :kpi_value="getKpiValue(kpi)"
        :account_currency_symbol="currencySymbol"
        :account_currency_code="account.currency_code"
        :account_id="account.id"
        :account_name="account.name"
        :account_timezone="account.timezone"
        :account_google_id="account.google_id"
        :account_is_enabled="accountIsEnabled"
        :is_synced="is_synced"
      />

      <div class="col w-full md:w-7/12">
        <div class="row">
          <div class="col w-full flex flex-wrap justify-between">
            <div class="px-2">
              <label class="block mb-2" for="username">BUDGET</label>
                <Tooltip
          :content=getBudgetTooltip
          :position="'center-left'"
          :underline="false"
          class="w-full"
          v-if="includeRollover"
        >
        <div v-if="includeRollover" class="absolute rollover_icon">
          <!-- <input type="text" id="input-budget" class="form-control w-full" value="£7,500.00" /> -->
          <i  class="fas fa-redo-alt" style="color:#02a27f;"></i>
                    </div>
              <CurrencyInput
                class="appearance-none border rounded w-26 py-3 px-3 leading-tight focus:outline-none focus:shadow-outline"
                type="text"
                v-model.number="combined_budget"
                v-on:input="settingChanged"
                v-currency="{ currency: account.currency_code }"
                @focus="changeToOriginalBudget"
                @blur="updateCombinedBudget"
              />
                </Tooltip>
              <CurrencyInput
                class="appearance-none border rounded w-26 py-3 px-3 leading-tight focus:outline-none focus:shadow-outline"
                type="text"
                v-model.number="budget"
                v-on:input="settingChanged"
                v-currency="{ currency: account.currency_code }"
                v-if="!includeRollover"

              />

            </div>

            <div class="px-2 flex-grow" style="max-width:100px;">
              <label class="block mb-2" for="username">KPI</label>
              <div class="relative">
                <select
                  class="block appearance-none w-full border py-3 px-3 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                  v-model="kpi"
                  @change="handleKpiUpdate"
                >
                  <option>{{ account.kpi_name.toUpperCase() }}</option>
                  <option>{{
                    account.kpi_name.toLowerCase() === "cpa" ? "ROAS" : "CPA"
                  }}</option>
                </select>
                <div
                  class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2"
                >
                  <svg
                    class="fill-current h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                  >
                    <path
                      d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"
                    />
                  </svg>
                </div>
              </div>
            </div>

            <div class="px-2">
              <label class="block mb-2" for="username"
                >{{ kpi.toUpperCase() }} TARGET</label
              >
              <CurrencyInput
                class="appearance-none border rounded w-24 py-3 px-3 leading-tight focus:outline-none focus:shadow-outline"
                type="text"
                v-model.number="kpi_target_value"
                v-on:input="settingChanged"
                v-currency="{ currency: account.currency_code }"
                v-if="kpi.toUpperCase()=='CPA'"
              />
              <CurrencyInput
                class="appearance-none border rounded w-24 py-3 px-3 leading-tight focus:outline-none focus:shadow-outline"
                type="text"
                v-model.number="kpi_target_value"
                v-on:input="settingChanged"
                v-currency="{ currency: {prefix:'',suffix:''} }"
                v-if="kpi.toUpperCase()=='ROAS'"

              />
            </div>

            <button
              class="py-3 px-8 rounded mt-auto"
              v-bind:class="[
                { 'cursor-not-allowed': !changed },
                { 'hover:bg-red-900': changed },
                { 'bg-gray-200 ': !changed },
                { 'bg-red650 ': changed },
                { 'text-white ': changed },
              ]"
              @click="handleBudgetSettingUpdate"
              :disabled="!changed"
            >
              {{ buttonText }}
            </button>
            <div class="flex flex-col justify-between">
              <Tooltip
                :class="'text-center cursor-default mx-auto'"
                :content="
                  'Enable or disable data syncronisation for this account. If you disable sync, we will not update this account and all AdEvolver features will be paused.'
                "
                :title="'Sync'"
                :position="'center-left'"
              />
              <div class="flex my-auto">
                <label
                  class="form-control w-16 h-8 bg-white"
                  @click="showAlert"
                >
                  <input
                    type="checkbox"
                    class="form-control switch"
                    @change="handleIsSyncedSettingUpdate"
                    v-model="is_synced"
                    :disabled="syncIsDisabled"
                  />
                  <span class="marker-bar m-auto"></span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card row" v-if="show_stats">
        <div class="card row">
          <div class="col w-full sm:w-1/2 md:w-1/3">
            <h2 class="block mb-2 text-lg font-semibold">Clicks</h2>
            <span class="font-semibold text-2xl">{{
              Number(getClicks).toLocaleString()
            }}</span>
          </div>
          <div class="col w-full sm:w-1/2 md:w-1/3">
            <h2 class="block mb-2 text-lg font-semibold">Impressions</h2>
            <span class="font-semibold text-2xl">{{
              Number(getImpressions).toLocaleString()
            }}</span>
          </div>
          <div class="col w-full sm:w-1/2 md:w-1/3">
            <h2 class="block mb-2 text-lg font-semibold">CTR</h2>
            <span class="font-semibold text-2xl">{{ getCtr }}%</span>
          </div>
        </div>

        <div class="card row">
          <div class="col w-full sm:w-1/2 md:w-1/3" v-if="kpi == 'CPA'">
            <h2 class="block mb-2 text-lg font-semibold">All Conversions</h2>
            <span class="font-semibold text-2xl">{{
              getAllConversions | number
            }}</span>
          </div>
          <div class="col w-full sm:w-1/2 md:w-1/3" v-else>
            <h2 class="block mb-2 text-lg font-semibold">All Conv. Value</h2>
            <span class="font-semibold text-2xl">{{
              getAllConversionValue | currency(account.account_currency_symbol)
            }}</span>
          </div>

          <div class="col w-full sm:w-1/2 md:w-1/3" v-if="kpi == 'CPA'">
            <h2 class="block mb-2 text-lg font-semibold">Conversions</h2>
            <span class="font-semibold text-2xl">{{
              getConversions | number
            }}</span>
          </div>
          <div class="col w-full sm:w-1/2 md:w-1/3" v-else>
            <h2 class="block mb-2 text-lg font-semibold">Conv. Value</h2>
            <span class="font-semibold text-2xl">{{
              getConversionValue | currency(account.account_currency_symbol)
            }}</span>
          </div>

          <div class="col w-full sm:w-1/2 md:w-1/3">
            <h2 class="block mb-2 text-lg font-semibold">{{ kpi }}</h2>
            <span class="font-semibold text-2xl">{{
              getKpiValue(kpi) | currency(account.account_currency_symbol)
            }}</span>
          </div>
        </div>
      </div>
      <div class='account_message' v-if='showAccountMessage'>
        <p>{{ account_message }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import AccountInfo from "./AccountInfo.vue";
import Tooltip from "@/components/common/Tooltip.vue";
import * as types from "@/store/modules/accounts/types";
import { mapActions, mapState, mapMutations } from "vuex";
import axios from "axios";

export default {
  name: "AccountItem",
  props: {
    account: {
      type: Object,
      required: true,
    },
  },
  components: {
    AccountInfo,
    Tooltip,
  },
  data() {
    return {
      buttonText: "Save Changes",
      changed: false,
      is_synced: this.account.is_synced == 0 ? false : true,
      ad_performance_report_processed_at: this.account
        .ad_performance_report_processed_at,
      budget: 0,
      kpi: this.account.kpi_name.toUpperCase() || 'CPA',
      kpi_target_value: Number(this.account.kpi_value),
      excess_budget: this.account.budget_commander ? Number(this.account.budget_commander.excess_budget) : 0,
      rollover_spend: this.account.budget_commander ? this.account.budget_commander.rollover_spend : 0,
      combined_budget: 0,
      show_budget: false, //without these the initial value (0) is overwriting the data value
      show_kpi_target_value: false, //without these the initial value (0) is overwriting the data value
      account_message: "",
      show_stats: false,
    };
  },
  created() {
    this.updateAccountMessage();
    this.assignBudgetValue()
    this.updateCombinedBudget()
  },
  computed: {
     ...mapState('accounts', [
      'number_of_synced_accounts'
    ]),
    getBudgetTooltip(){
      const date = new Date()
      const month = date.toLocaleString('default', { month: 'long' });
      return this.currencySymbol + this.excess_budget.toLocaleString() + ' of unspent budget rolled over from last month. Your budget for '+month+' is '+this.currencySymbol+(this.budget+this.excess_budget).toLocaleString()
    },
    currencySymbol(){
      return this.account.currency[this.account.currency_code].symbol
    },
    includeRollover(){
      return this.rollover_spend&&this.excess_budget>0
    },
    getPerformance() {
      return this.account.performance.length > 0
        ? this.account.performance[0]
        : false;
    },
    getSpend: function() {
      if (!this.getPerformance) return 0;
      return Number(this.getPerformance["cost"]);
    },
    getClicks: function() {
      if (!this.getPerformance) return 0;
      return this.getPerformance["clicks"];
    },
    getImpressions: function() {
      if (!this.getPerformance) return 0;
      return this.getPerformance["impressions"];
    },
    getCtr: function() {
      if (!this.getPerformance) return 0;
      return this.getPerformance["ctr"];
    },
    getAllConversions: function() {
      if (!this.getPerformance) return 0;
      return this.getPerformance["conversions"];
    },
    getAllConversionValue: function() {
      if (!this.getPerformance) return 0;
      return this.getPerformance["conversion_value"];
    },
    getConversions: function() {
      if (!this.getPerformance) return 0;
      return this.getPerformance["conversions"];
    },
    getConversionValue: function() {
      if (!this.getPerformance) return 0;
      return this.getPerformance["conversion_value"];
    },
    accountIsEnabled() {
      //true if the account is synced and the data has processed for the first time
      if (!this.is_synced) return false;
      if (!this.ad_performance_report_processed_at) return false; //TODO check this works
      return true;
    },
    getKpiValue: function() {
      return (kpiValue) => {
        const performance_available = this.account.performance.length > 0;
        const cpa = performance_available
          ? Number(this.account.performance[0].cpa)
          : 0;
        const roas = performance_available
          ? Number(this.account.performance[0].roas)
          : 0;
        return kpiValue.toLowerCase() === "cpa" ? cpa : roas;
      };
    },
    syncIsDisabled() {
      if (this.changed && !this.is_synced) {
        return true;
      }
      if ((!this.hasBudget || !this.hasKpiTargetValue) && !this.is_synced) {
        return true;
      }
      if(this.number_of_synced_accounts > 0 && !this.is_synced){
        return true
      }

      return false;
    },
    hasBudget() {
      return this.budget > 0;
    },
    hasKpiTargetValue() {
      return this.kpi_target_value > 0;
    },
    showAccountMessage(){
      return !(this.is_synced && this.ad_performance_report_processed_at)
    }
  },
  methods: {
    ...mapActions("accounts", [types.UPDATE_ACCOUNT_BUDGET_SETTING,types.GET_NUMBER_OF_SYNCED_ACCOUNTS]),
    ...mapActions([
      "createAlert", 
      "setBudgetCommanderBudget",
      "setBudgetCommanderKpiTarget",
      "setBudgetCommanderKpiOption",
      ]),
    ...mapMutations("accounts", [types.TOGGLE_SYNC_SUCCESS]),
    toggleShowStats() {
      this.show_stats = !this.show_stats;
    },
    updateAccountMessage() {
      if (!this.is_synced)
        this.account_message = "Toggle sync on to access this account";
      if (this.is_synced && !this.ad_performance_report_processed_at)
        this.account_message = "Please wait whilst we sync this account";
    },
    showAlert() {
      if (this.syncIsDisabled) {

        let payload = {
          headline: "Please set a budget & kpi for this account",
          message:
            "We'll need them to calculate suggestions. You can change these later.",
          dismissSecs: 5,
        }

        if(this.number_of_synced_accounts > 0){
          payload = {
          headline: "Maximum number of accounts exceeded",
          message:
            "Only a single account is available during the early access period.",
          dismissSecs: 5,
          }
        }

        this.createAlert(payload);
      }
    },
    handleIsSyncedSettingUpdate() {
      let maximum_accounts = 1; //hard-coded for now but this will use the subscription settings
      this.updateAccountMessage();

      axios.get("/api/account/" + this.account.id + "/toggle_is_synced").then(()=> {
        this[types.GET_NUMBER_OF_SYNCED_ACCOUNTS](this.account.user_id);
      });

      this[types.TOGGLE_SYNC_SUCCESS]({
        id: this.account.id,
        is_synced: this.is_synced,
      });

    },
    handleBudgetSettingUpdate() {
      const payload = {
        budget: this.budget,
        kpi_name: this.kpi,
        kpi_value: this.kpi_target_value,
        account_id: this.account.id,
        is_synced: this.is_synced,
      };
      this[types.UPDATE_ACCOUNT_BUDGET_SETTING](payload);
      this.setBudgetCommanderBudget(this.budget)
      this.setBudgetCommanderKpiTarget(this.kpi_target_value)
      this.setBudgetCommanderKpiOption(this.kpi)
      this.buttonText = "Changed saved!";
      setTimeout(() => {
        this.buttonText = "Save Changes";
        this.changed = false;
      }, 2000);
    },
    settingChanged() {
      this.changed = true;
    },
    handleKpiUpdate() {
      this.changed = true;
      this.kpi_value = this.getKpiValue(this.kpi);
    },
    changeToOriginalBudget(){
      //when the user edits the budget they're editing the original budget excluding the rollover
      this.combined_budget = this.budget
    },
    updateCombinedBudget(event){
      if(event){
        this.budget = Number(event.target.value)
      }
      this.combined_budget = this.budget + this.excess_budget
    },
    assignBudgetValue(){
      this.budget = Number(this.account.budget)
    }
  },
};
</script>

<style scoped>
.account_message {
  width: 100%;
  text-align: center;
  border-radius: 6px;
}

.rollover_icon{
    right: 10px;
    top: 10px;
}

</style>
