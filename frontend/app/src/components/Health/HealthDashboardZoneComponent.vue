<template>
    <div class="col">
        <div class="card mb-3 text-center shadow-sm">
            <div class="card-header">
                <h4>{{ $t("healthDashboardZoneComponent.weight") }}</h4>
            </div>
            <div class="card-body">
                <h1 v-if="currentWeight && Number(authStore?.user?.units) === 1">{{ currentWeight }} {{ $t("generalItems.unitsKg") }}</h1>
                <h1 v-else-if="currentWeight && authStore.user.units == 2">{{ kgToLbs(currentWeight) }} {{ $t("generalItems.unitsLbs") }}</h1>
                <h1 v-else>{{ $t("generalItems.labelNotApplicable") }}</h1>
            </div>
            <div class="card-footer text-body-secondary">
                <span v-if="userHealthTargets && userHealthTargets['weight']">{{ userHealthTargets.weight }}</span>
                <span v-else>{{ $t("healthDashboardZoneComponent.noWeightTarget") }}</span>
            </div>
        </div>
    </div>
    <div class="col">
        <div class="card mb-3 text-center shadow-sm">
            <div class="card-header">
                <h4>{{ $t("healthDashboardZoneComponent.bmi") }}</h4>
            </div>
            <div class="card-body">
                <h1 v-if="currentBMI">{{ currentBMI }}</h1>
                <h1 v-else>{{ $t("generalItems.labelNotApplicable") }}</h1>
            </div>
            <div class="card-footer text-body-secondary">
                <span v-if="currentBMI">{{ bmiDescription }}</span>
                <span v-else-if="!currentBMI && currentWeight">{{ $t("healthDashboardZoneComponent.noHeightDefined") }}</span>
                <span v-else>{{ $t("healthDashboardZoneComponent.noWeightData") }}</span>
            </div>
        </div>
    </div>
    <div class="col">
        <div class="card mb-3 text-center shadow-sm">
            <div class="card-header">
                <h4>{{ $t("healthDashboardZoneComponent.vo2max") }}</h4>
            </div>
            <div class="card-body">
                <h1 v-if="currentVo2Max">{{ currentVo2Max }}</h1>
                <h1 v-else>{{ $t("generalItems.labelNotApplicable") }}</h1>
            </div>
            <div class="card-footer text-body-secondary">
                <span v-if="currentVo2Max">{{ vo2maxDescription }}</span>
                <span v-else>{{ $t("healthDashboardZoneComponent.noVo2MaxData") }}</span>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
// Importing the stores
import { useAuthStore } from "@/stores/authStore";
import { kgToLbs } from "@/utils/unitsUtils";
import vo2maxRanges from "@/components/Health/HealthVO2MaxRanges.json"
export default {
    components: {
        
    },
    props: {
        user: {
            type: [Object, null],
            required: true
        },
        userHealthData: {
            type: [Object, null],
            required: true,
        },
        userHealthTargets: {
            type: [Object, null],
            required: true,
        },
    },
    setup(props) {
        const { t } = useI18n();
        const authStore = useAuthStore();
        const currentWeight = ref(null);
        const currentBMI = ref(null);
        const bmiDescription = ref(null);
        const currentVo2Max = ref(null);
        const vo2maxDescription = ref(null);
        const vo2maxRange = null;

        onMounted(async () => {
            if(props.userHealthData){
                for(const data of props.userHealthData){
                    if(data.weight){
                        currentWeight.value = data.weight;
                        currentBMI.value = data.bmi;
                        currentVo2Max.value = data.vo2max;
                        break;
                    }
                }

                if(currentBMI.value){
                    if(currentBMI.value < 18.5){
                        bmiDescription.value = t("healthDashboardZoneComponent.bmiUnderweight");
                    } else if(currentBMI.value >= 18.5 && currentBMI.value < 24.9){
                        bmiDescription.value = t("healthDashboardZoneComponent.bmiNormalWeight");
                    } else if(currentBMI.value >= 25 && currentBMI.value < 29.9){
                        bmiDescription.value = t("healthDashboardZoneComponent.bmiOverweight");
                    } else if(currentBMI.value >= 30 && currentBMI.value < 34.9){
                        bmiDescription.value = t("healthDashboardZoneComponent.bmiObesityClass1");
                    } else if(currentBMI.value >= 35 && currentBMI.value < 39.9){
                        bmiDescription.value = t("healthDashboardZoneComponent.bmiObesityClass2");
                    } else if(currentBMI.value >= 40){
                        bmiDescription.value = t("healthDashboardZoneComponent.bmiObesityClass3");
                    }
                }

                if (currentVo2Max.value){
                    
                    const vo2MaxRange = vo2maxRanges.MALE["20-29"]
                    for (const key in vo2MaxRange) {
                        const vo2Data = vo2MaxRange[key];
                        if (vo2Data.max !== null && vo2Data.min !== null && currentVo2Max.value > vo2Data.min && currentVo2Max.value <= vo2Data.max) {
                            vo2maxDescription.value = t(vo2Data.category);
                            break;
                        }
                        if (vo2Data.max !== null && vo2Data.min === null && currentVo2Max.value <= vo2Data.max) {
                            vo2maxDescription.value = t(vo2Data.category);
                            break;
                        }
                        if (vo2Data.max === null && vo2Data.min !== null && currentVo2Max.value >= vo2Data.min) {
                            vo2maxDescription.value = t(vo2Data.category);
                            break;
                        }
                    }
                }
            }
        });


        return {
            authStore,
            currentWeight,
            currentBMI,
            bmiDescription,
            kgToLbs,
            currentVo2Max,
            vo2maxDescription
        };
    },
};
</script>