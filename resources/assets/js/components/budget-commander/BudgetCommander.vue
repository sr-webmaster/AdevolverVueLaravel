<template>
  <!-- Budget Commander View -->
  <div class="BudgetCommander w-full">
    <main class="minimized">
      <div class="row">
        <!-- Budget Commander Summary -->
        <BudgetCommanderSummary
          :budget="budget"
          :average_cpc="average_cpc"
          :required_cpc="required_cpc"
          :kpi_value="cpa"
          :kpi-option="kpiOption"
          :kpi-target="kpiTarget"
          :account="account"
          :rollover_spend="budget_commander_rollover_spend"
          v-if="dataDownloadedSuccessfully"
        />
        <!-- Summary Graph -->
        <BudgetCommanderChartWrapper
          :budget="budget"
          :kpi-target="kpiTarget"
          :account="account"
          :rollover_spend="budget_commander_rollover_spend"
          :excess_budget="excessBudget"
        />

        <div class="col w-full lg:w-1/2 xl:w-1/3">
          <div class="card BudgetCommander__settings">
            <!-- Budget Commander Settings -->
            <BudgetCommanderSettings
              :account="account"
              @budgetUpdated="updateBudget"
              @kpiOptionUpdated="updateKPIOption"
              @kpiTargetUpdated="updateKPITarget"
            />

            <!-- Budget Commander Actions -->
            <BudgetCommanderActions
              :account="account"
            />
          </div>
        </div>

        <!-- <EmptyGroup 
          class="BudgetCommander__group" 
          v-if="groupState === 'empty'" 
          @createNewGroup="showCreateGroupSection"
        />

        <CreateGroup
          v-else-if="groupState === 'create'"
        /> -->
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import BudgetCommanderSettings from "./BudgetCommanderSettings.vue"
import BudgetCommanderSummary from "./BudgetCommanderSummary.vue"
import BudgetCommanderActions from "./BudgetCommanderActions.vue"
import BudgetCommanderChartWrapper from "./BudgetCommanderChartWrapper.vue"
import EmptyGroup from "./budgetGroups/EmptyGroup.vue"
import CreateGroup from "./budgetGroups/CreateGroup.vue"
import { 
  mapState, 
  mapGetters, 
  mapActions 
} from "vuex";

export default {
  name: "budget-commander",
  data () {
    return {
      budget: 0,
      kpiOption: 'CPA',
      kpiTarget: 0,
      account: this.$route.params.id,
      average_cpc: 0,
      required_cpc: 0,
      cpa: 0,
      groupState : 'empty'
    }
  },
  components: {
    BudgetCommanderSummary,
    BudgetCommanderSettings,
    BudgetCommanderActions,
    BudgetCommanderChartWrapper,
    EmptyGroup,
    CreateGroup,
  },
  async mounted () {
    // Get Budget
    await axios.get('/api/account/' + this.account + '/budget').then(response => {
      this.results = response.data;
      this.budget = Number(this.results.data.budget);
      this.setBudgetCommanderBudget(this.budget)
    }, error => {
      console.error(error)
      if(error.response && error.response.status >= 400){
        window.location.replace('/404');
      }
    });

    // Get KPI type and target
    await axios.get('/api/account/' + this.account + '/kpi').then(response => {
      this.results = response.data;
      this.kpiOption = this.results.data.kpi_name.toUpperCase()
      this.kpiTarget = Number(this.results.data.kpi_value);
      this.setBudgetCommanderKpiTarget(this.kpiTarget)
      this.setBudgetCommanderKpiOption(this.kpiOption)
    });

    //    // Get cpa and average_cpc
    // await axios.get('/api/account/' + this.account + '/bcgraph').then(response => {
    //   this.results = response.data;
    //   this.average_cpc = Number(this.results.performance[0].average_cpc);
    //   this.cpa = Number(this.results.performance[0].cpa);
    // });

    this.getBudgetCommanderData({
      account_id: this.account
    });

    this.groupState = this.groupList.length === 0 ? 'empty' : 'list'
  },
  methods: {
    ...mapActions([
      "getBudgetCommanderData",
      'setBudgetCommanderBudget',
      'setBudgetCommanderKpiOption',
      'setBudgetCommanderKpiTarget',
      ]),

    // Update Budget
    updateBudget (budget) {
      this.budget = parseFloat(budget);
    },
    // Update KPI type
    updateKPIOption (option) {
      this.kpiOption = option
    },
    // Update KPI Target
    updateKPITarget (target) {
      this.kpiTarget = parseFloat(target)
    },

    showCreateGroupSection () {
      this.groupState = 'create'
    }
  },
  computed: {
    ...mapState({
      groupList: state => state.budget_commander.groupList
    }),
    ...mapGetters(["budget_commander_response_data", 
    "budget_commander_data_state", 
    "budget_commander_promise",
    "budget_commander_rollover_spend",
    "budget_commander_excess_budget"
    ]),
    dataDownloadedSuccessfully(){
      return this.budget_commander_data_state.isSuccess
    },
    excessBudget(){
      return this.budget_commander_excess_budget
    },
  }
}
</script>

<style scoped>

</style>
