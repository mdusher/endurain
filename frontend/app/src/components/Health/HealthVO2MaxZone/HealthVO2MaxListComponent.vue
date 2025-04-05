<template>
    <li class="list-group-item d-flex justify-content-between p-0 bg-body-tertiary">
        <div class="d-flex align-items-center">
            <font-awesome-icon :icon="['fas', 'person-running']" size="2x" />
            <div class="ms-3">
                <div class="fw-bold">
                    <span>{{ data.vo2max }}</span>
                </div>
                <span>
                    Date: {{ formatDateShort(data.date) }}
                </span>
            </div>
        </div>
        <div>
            <!--<span class="badge bg-primary-subtle border border-primary-subtle text-primary-emphasis align-middle ms-2" v-if="data.garminconnect_body_composition_id">{{ $t("healthVO2MaxListComponent.labelGarminConnect") }}</span>-->
            <span class="align-middle me-3 d-none d-sm-inline" v-if="data.garminconnect_body_composition_id">
                <img src="/src/assets/garminconnect/Garmin_Connect_app_1024x1024-02.png" alt="Garmin Connect logo" height="22" />
            </span>
        </div>
    </li>
</template>

<script>
import { useI18n } from "vue-i18n";
// Importing the stores
import { useAuthStore } from "@/stores/authStore";
// Import Notivue push
import { push } from "notivue";
// Importing the services
import { health_data } from "@/services/health_dataService";
// Import the components
import ModalComponent from '@/components/Modals/ModalComponent.vue';

import { formatDateShort } from "@/utils/dateTimeUtils";

export default {
    components: {
        ModalComponent,
    },
    props: {
        data: {
            type: Object,
            required: true,
        },
    },
    emits: ["editedVO2Max", "deletedVO2Max"],
    setup(props, { emit } ) {
        const { t } = useI18n();
        const authStore = useAuthStore();

        async function updateVO2MaxListEdited(editedVO2Max){
            try {
                await health_data.editHealthData(editedVO2Max);

                emit("editedVO2Max", editedVO2Max);

                push.success(t("healthVO2MaxListComponent.successEditVO2Max"));
            } catch (error) {
                push.error(`${t("healthVO2MaxListComponent.errorEditVO2Max")} - ${error.toString()}`);
            }
        }

        async function submitDeleteVO2Max(){
            try {
                const data = {
                    id: props.data.id,
                    user_id: props.data.user_id,
                    VO2Max: null,
                    bmi: null,
                };
                await health_data.editHealthData(data);

                emit("deletedVO2Max", data.id);

                push.success(t("healthVO2MaxListComponent.successDeleteVO2Max"));
            } catch (error) {
                push.error(`${t("healthVO2MaxListComponent.errorDeleteVO2Max")} - ${error.toString()}`);
            }
        }

        return {
            t,
            authStore,
            updateVO2MaxListEdited,
            submitDeleteVO2Max,
            formatDateShort,
        };
    },
};
</script>