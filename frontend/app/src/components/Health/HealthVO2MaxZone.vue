<template>
    <div class="col">
        <LoadingComponent v-if="isLoading" />
        <div v-else>
            <!-- Checking if dataWithVO2Max is loaded and has length -->
            <div v-if="dataWithVO2Max && dataWithVO2Max.length" class="mt-3 p-3 bg-body-tertiary rounded shadow-sm">
                <!-- show graph -->
                <HealthVO2MaxLineChartComponent :userHealthData="dataWithVO2Max" :isLoading="isLoading" />

                <br>
                <p>{{ $t("healthVO2MaxZoneComponent.labelNumberOfHealthDataVO2Max1") }}{{ userHealthData.length }}{{ $t("healthVO2MaxZoneComponent.labelNumberOfHealthDataVO2Max2") }}{{ userHealthDataPagination.length }}{{ $t("healthVO2MaxZoneComponent.labelNumberOfHealthDataVO2Max3") }}</p>

                <!-- Displaying loading new gear if applicable -->
                <ul class="mt-3 list-group list-group-flush" v-if="isLoadingNewVO2Max">
                        <li class="list-group-item rounded">
                            <LoadingComponent />
                        </li>
                    </ul>

                <!-- list zone -->
                <ul class="my-3 list-group list-group-flush"  v-for="data in dataWithVO2MaxPagination" :key="data.id" :data="data">
                    <HealthVO2MaxListComponent :data="data" @deletedVO2Max="updateVO2MaxListDeleted" @editedVO2Max="updateVO2MaxListEdited" />
                </ul>

                <!-- pagination area -->
                <PaginationComponent :totalPages="totalPages" :pageNumber="pageNumber" @pageNumberChanged="setPageNumber" />
            </div>
            <!-- Displaying a message or component when there are no VO2Max measurements -->
            <div v-else class="mt-3">
                <br>
                <NoItemsFoundComponent />
            </div>
        </div>
    </div>
</template>

<script>
import { ref, watchEffect, onMounted } from "vue";
import HealthVO2MaxLineChartComponent from './HealthVO2MaxZone/HealthVO2MaxLineChartComponent.vue';
import HealthVO2MaxListComponent from './HealthVO2MaxZone/HealthVO2MaxListComponent.vue';
import LoadingComponent from '../GeneralComponents/LoadingComponent.vue';
import NoItemsFoundComponent from '../GeneralComponents/NoItemsFoundComponents.vue';
import PaginationComponent from '../GeneralComponents/PaginationComponent.vue';

export default {
    components: {
        HealthVO2MaxLineChartComponent,
        HealthVO2MaxListComponent,
        LoadingComponent,
        NoItemsFoundComponent,
        PaginationComponent,
    },
    props: {
        userHealthData: {
            type: [Object, null],
            required: true,
        },
        userHealthDataPagination: {
            type: [Object, null],
            required: true,
        },
        userHealthTargets: {
            type: [Object, null],
            required: true,
        },
        isLoading: {
            type: Boolean,
            required: true,
        },
        totalPages: {
            type: Number,
            required: true,
        },
        pageNumber: {
            type: Number,
            required: true,
        },
    },
    emits: ["pageNumberChanged"],
    setup(props, { emit }) {
        const dataWithVO2Max = ref([]);
        const dataWithVO2MaxPagination = ref([]);
        
        const isLoadingNewVO2Max = ref(false);

        function updateddataWithVO2MaxArray(){
            dataWithVO2MaxPagination.value = [];
            dataWithVO2Max.value = [];
            if(props.userHealthDataPagination){
                for(const data of props.userHealthDataPagination){
                    if(data.vo2max){
                        dataWithVO2MaxPagination.value.push(data)
                    }
                }
            }
            if(props.userHealthData){
                for(const data of props.userHealthData){
                    if(data.vo2max){
                        dataWithVO2Max.value.push(data)
                    }
                }
            }
        }

        function updateIsLoadingNewVO2Max(isLoadingNewVO2MaxNewValue) {
            isLoadingNewVO2Max.value = isLoadingNewVO2MaxNewValue;
        }

        function setPageNumber(page) {
            // Set the page number.
            emit("pageNumberChanged", page);
        }

        watchEffect(() => {
            if (props.userHealthDataPagination) {
                updateddataWithVO2MaxArray();
            }
        });

        onMounted(() => {
            updateddataWithVO2MaxArray();
        });

        return {
            dataWithVO2Max,
            dataWithVO2MaxPagination,
            isLoadingNewVO2Max,
            updateIsLoadingNewVO2Max,
            setPageNumber,
        };
    },
};
</script>