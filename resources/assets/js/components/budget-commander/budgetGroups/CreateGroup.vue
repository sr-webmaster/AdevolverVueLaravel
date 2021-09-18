<template>
  <div class="col w-full">
    <div class="card">
      <div class="row">
        <div class="col w-full lg:w-1/2 xl:w-2/3">
          <div class="card">
            <div class="card-title flex justify-between">
              Creating a new Budget Group
              <Search
                placeholder="Search"
                @handleSearchInput="debounceSearch"
              />
            </div>
            <div class="card-body w-full">
              <table class="w-full mt-10">
                <thead>
                  <tr>
                    <th class="w-1/12 border border-t-0 border-l-0 border-gray-400 px-4 py-2">
                      <div class="flex my-auto">
                        <label class="form-control w-16 h-8 bg-white">
                          <input
                            type="checkbox"
                            class="form-control switch"
                            v-model="allSelected"
                          />
                          <span class="marker-bar m-auto"></span>
                        </label>
                      </div>
                    </th>
                    <th class="w-5/12 border border-t-0 border-gray-400 px-4 py-2 text-left">
                      Campaign
                    </th>
                    <th class="w-2/12 border border-t-0 border-gray-400 px-4 py-2">
                      Campaign Type
                    </th>
                    <th class="w-4/12 border border-t-0 border-r-0 border-gray-400 px-4 py-2 text-left">
                      Existing Budget Group
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td class="border border-l-0 border-gray-400 px-4 py-2">
                      <div class="flex my-auto">
                        <label class="form-control w-16 h-8 bg-white">
                          <input
                            type="checkbox"
                            class="form-control switch"
                            :key="1"
                            :checked="allSelected"
                            @change="handleSelectCampaign"
                          />
                          <span class="marker-bar m-auto"></span>
                        </label>
                      </div>
                    </td>
                    <td class="border border-gray-400 px-4 py-2 text-left text-red650">Campaign1</td>
                    <td class="border border-gray-400 px-4 py-2 text-center">asdf</td>
                    <td class="border border-r-0 border-gray-400 px-4 py-2 text-left text-red650">Group1</td>
                  </tr>
                  <tr>
                    <td class="border border-l-0 border-gray-400 px-4 py-2">
                      <div class="flex my-auto">
                        <label class="form-control w-16 h-8 bg-white">
                          <input
                            type="checkbox"
                            class="form-control switch"
                            :key="2"
                            :checked="allSelected"
                            @change="handleSelectCampaign"
                          />
                          <span class="marker-bar m-auto"></span>
                        </label>
                      </div>
                    </td>
                    <td class="border border-gray-400 px-4 py-2 text-left text-red650">Campaign2</td>
                    <td class="border border-gray-400 px-4 py-2 text-center">asdf</td>
                    <td class="border border-r-0 border-gray-400 px-4 py-2 text-left text-red650">Group2</td>
                  </tr>
                  <tr>
                    <td class="border border-l-0 border-gray-400 px-4 py-2">
                      <div class="flex my-auto">
                        <label class="form-control w-16 h-8 bg-white">
                          <input
                            type="checkbox"
                            class="form-control switch"
                            :key="3"
                            :checked="allSelected"
                            @change="handleSelectCampaign"
                          />
                          <span class="marker-bar m-auto"></span>
                        </label>
                      </div>
                    </td>
                    <td class="border border-gray-400 px-4 py-2 text-left text-red650">Campaign3</td>
                    <td class="border border-gray-400 px-4 py-2 text-center">asdf</td>
                    <td class="border border-r-0 border-gray-400 px-4 py-2 text-left text-red650">Group3</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="col w-full lg:w-1/2 xl:w-1/3">
          <div class="card">
            <div class="card-title">
              Budget Group Settings
            </div>
            <div class="card-body">
              <div class="form-row">
                <label class="w-1/3 mr-6" for="input-budget">Budget Name</label>
                <div class="flex-grow relative">
                  <input
                    class="form-control w-full"
                    :value="group_budget_name"
                  />
                </div>
              </div>
              <div class="form-row">
                <label class="w-1/3 mr-6" for="input-budget">Target Spend</label>
                <div class="flex-grow relative">
                  <CurrencyInput
                    :currency="currencyCode"
                    :value="group_budget_spend"
                    class="form-control w-full"
                    locale="en"
                  />
                </div>
              </div>

              <div class="form-row">
                <label class="w-1/3 mr-6">Target KPI</label>
                <div class="flex-grow flex flex-no-wrap">
                  <input class="form-control danger" type="radio" name="radio-inline"
                    id="group_cpa"
                    value="CPA"
                    v-model="group_kpi_option"
                  >
                  <label for="group_cpa" class="mr-4">CPA</label>
                  <input class="form-control dark" type="radio" name="radio-inline"
                    id="group_roas"
                    value="ROAS"
                    v-model="group_kpi_option"
                  >
                  <label for="group_roas">ROAS</label>
                </div>
              </div>

              <div class="form-row">
                <label class="w-1/3 mr-6" for="input-kpi-target">{{group_kpi_option}} Target</label>
                <div class="flex-grow">
                  <CurrencyInput
                    :currency="currencyCode"
                    :value="group_kpi_target_value"
                    class="form-control w-full"
                    locale="en"
                    />
                </div>
              </div>
              <div class="flex justify-center mt-12 mb-6">
                <button 
                  class="red-primary"
                >
                  Save Budget
                </button>
                <button 
                  class="py-3 px-8 m-1 rounded bg-gray-200"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex'
import { debounce } from 'debounce'
import { DEBOUNCE } from '@/config/constants'
import Search from '@/components/common/Search.vue'

export default {
  name: "CreateGroup",
  components: {
    Search
  },
  data() {
    return {
      group_budget_name: '',
      group_budget_spend: 0,
      group_kpi_option: 'CPA',
      group_kpi_target_value: 0,
      search: '',
      allSelected: false,
      selectedCampaigns: []
    }
  },
  created () { 
    this.debounceSearch = debounce( e => {
    }, DEBOUNCE.DEFAULT)
  },
  computed: {
    ...mapGetters([
      'selected_account',
    ]),
    currencyCode(){
      return this.selected_account.account_currency_code
    },
  },
  methods: {
    handleSelectCampaign: function () {

    }
  }
}
</script>

<style scoped>

</style>