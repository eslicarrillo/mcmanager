<template>
  <div>
    <h1>Visor de Datos</h1>
    <div>
      <label for="table-select">Seleccione una tabla:</label>
      <select id="table-select" v-model="selectedTable" @change="fetchData">
        <option v-for="table in tables" :key="table" :value="table">
          {{ table }}
        </option>
      </select>
    </div>

    <div v-if="selectedTable">
      <h2>Datos de la tabla: {{ selectedTable }}</h2>
      <table>
        <thead>
          <tr>
            <th v-for="(value, key) in tableColumns" :key="key">{{ key }}</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <!-- Formulario de Alta -->
          <tr>
            <td v-for="(value, key) in newRecord" :key="key">
              <div v-if="isForeignKey(key)">
                <select v-model="newRecord[key]">
                  <option v-for="(name, id) in relatedData[key]" :key="id" :value="id">{{ name }}</option>
                </select>
              </div>
              <div v-else>
                <input
                  type="text"
                  v-model="newRecord[key]"
                  :size="newRecord[key]?.toString().length || 1"
                />
              </div>
            </td>
            <td>
              <button @click="addNewRecord">Agregar</button>
            </td>
          </tr>
          <!-- Datos de la Tabla -->
          <tr v-for="(item, index) in data" :key="item.id">
            <td v-for="(value, key) in item" :key="key">
              <div v-if="isForeignKey(key)">
                {{ getRelatedName(key, value) }}
              </div>
              <div v-else>
                <input
                  type="text"
                  v-model="data[index][key]"
                  :size="data[index][key]?.toString().length || 1"
                />
              </div>
            </td>
            <td>
              <button @click="saveData(item.id, index)">Guardar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>No se encontraron datos para la tabla seleccionada.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tables: ['ooads', 'unidades', 'criterios', 'subcriterios', 'acciones', 'seguimientos', 'bandas', 'subbandas', 'users'],
      selectedTable: '',
      data: [],
      newRecord: {},
      relatedData: {},
      tableColumns: {}
    };
  },
  methods: {
    async fetchData() {
      if (this.selectedTable) {
        try {
          const response = await axios.get(`http://localhost:8000/api/${this.selectedTable}/`);
          this.data = response.data;
          this.initializeNewRecord();
          await this.fetchRelatedData();
          this.setTableColumns();
        } catch (error) {
          console.error(`Error fetching data from ${this.selectedTable}:`, error);
          this.data = [];
          this.initializeNewRecord();
        }
      }
    },
    async saveData(id, index) {
      if (this.selectedTable && id) {
        try {
          const response = await axios.put(`http://localhost:8000/api/${this.selectedTable}/${id}/`, this.data[index]);
          console.log('Datos guardados exitosamente:', response.data);
        } catch (error) {
          console.error(`Error saving data for ${this.selectedTable} with ID ${id}:`, error);
        }
      }
    },
    async addNewRecord() {
      if (this.selectedTable) {
        try {
          const response = await axios.post(`http://localhost:8000/api/${this.selectedTable}/`, this.newRecord);
          this.data.push(response.data);
          this.initializeNewRecord();
        } catch (error) {
          console.error(`Error adding new record to ${this.selectedTable}:`, error);
        }
      }
    },
    initializeNewRecord() {
      if (this.data.length > 0) {
        this.newRecord = Object.keys(this.data[0]).reduce((acc, key) => {
          acc[key] = '';
          return acc;
        }, {});
      } else {
        // Si no hay datos, inicializamos el formulario con las columnas de la tabla
        this.newRecord = Object.keys(this.tableColumns).reduce((acc, key) => {
          acc[key] = '';
          return acc;
        }, {});
      }
    },
    async fetchRelatedData() {
      this.relatedData = {};
      // Obtener datos relacionados dependiendo de la tabla seleccionada
      if (['unidades', 'criterios', 'subcriterios', 'acciones'].includes(this.selectedTable)) {
        const responseOOAD = await axios.get(`http://localhost:8000/api/ooads/`);
        this.relatedData['ooad_id'] = responseOOAD.data.reduce((acc, ooad) => {
          acc[ooad.id] = ooad.name;
          return acc;
        }, {});
      }
      if (['criterios', 'subcriterios', 'acciones'].includes(this.selectedTable)) {
        const responseUnidad = await axios.get(`http://localhost:8000/api/unidades/`);
        this.relatedData['unidad_id'] = responseUnidad.data.reduce((acc, unidad) => {
          acc[unidad.id] = unidad.name;
          return acc;
        }, {});
      }
      if (['subcriterios', 'acciones'].includes(this.selectedTable)) {
        const responseCriterio = await axios.get(`http://localhost:8000/api/criterios/`);
        this.relatedData['criterio_id'] = responseCriterio.data.reduce((acc, criterio) => {
          acc[criterio.id] = criterio.name;
          return acc;
        }, {});
      }
      if (['acciones'].includes(this.selectedTable)) {
        const responseSubcriterio = await axios.get(`http://localhost:8000/api/subcriterios/`);
        this.relatedData['subcriterio_id'] = responseSubcriterio.data.reduce((acc, subcriterio) => {
          acc[subcriterio.id] = subcriterio.name;
          return acc;
        }, {});
      }
    },
    isForeignKey(key) {
      // Implementa la lógica para identificar claves foráneas
      // Por ejemplo, si las claves foráneas siempre terminan en '_id':
      return key.endsWith('_id');
    },
    getRelatedName(key, value) {
      return this.relatedData[key] ? this.relatedData[key][value] : value;
    },
    setTableColumns() {
      if (this.data.length > 0) {
        this.tableColumns = this.data[0];
      } else {
        // Si no hay datos, podemos definir manualmente las columnas según la tabla seleccionada
        const columnMap = {
          ooads: { id: '', name: '' },
          unidades: { id: '', name: '', ooad_id: '' },
          criterios: { id: '', name: '', unidad_id: '' },
          subcriterios: { id: '', name: '', criterio_id: '' },
          acciones: { id: '', name: '', subcriterio_id: '' },
          seguimientos: { id: '', accion_id: '', progress: '', status: '' },
          bandas: { id: '', name: '' },
          subbandas: { id: '', name: '', banda_id: '' },
          users: { id: '', username: '', email: '', role: '' },
        };
        this.tableColumns = columnMap[this.selectedTable] || {};
      }
    }
  },
  watch: {
    selectedTable(newTable, oldTable) {
      if (newTable !== oldTable) {
        this.fetchData();
      }
    }
  }
};
</script>

<style>
table {
  width: 100%;
  border-collapse: collapse;
}

table, th, td {
  border: 1px solid black;
}

th, td {
  padding: 8px;
  text-align: left;
}

input, select {
  box-sizing: border-box;
}
</style>
