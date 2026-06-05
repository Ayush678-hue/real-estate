import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Search, MapPin, Bed, Bath, Maximize, SlidersHorizontal, RefreshCw } from 'lucide-react';
import { propertyService } from '../api';
import './Properties.css';

const Properties = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showMobileFilters, setShowMobileFilters] = useState(false);

  // States mirroring backend API filters
  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [city, setCity] = useState(searchParams.get('city') || '');
  const [propertyType, setPropertyType] = useState(searchParams.get('property_type') || '');
  const [bedrooms, setBedrooms] = useState(searchParams.get('bedrooms') || '');
  const [listingType, setListingType] = useState(searchParams.get('listing_type') || '');
  const [priceMin, setPriceMin] = useState(searchParams.get('price_min') || '');
  const [priceMax, setPriceMax] = useState(searchParams.get('price_max') || '');

  // Synchronize state with URL parameters when URL changes
  useEffect(() => {
    setSearch(searchParams.get('search') || '');
    setCity(searchParams.get('city') || '');
    setPropertyType(searchParams.get('property_type') || '');
    setBedrooms(searchParams.get('bedrooms') || '');
    setListingType(searchParams.get('listing_type') || '');
    setPriceMin(searchParams.get('price_min') || '');
    setPriceMax(searchParams.get('price_max') || '');
  }, [searchParams]);

  // Fetch properties based on filters
  const fetchProperties = async () => {
    setLoading(true);
    try {
      const params = {};
      if (search) params.search = search;
      if (city) params.city = city;
      if (propertyType) params.property_type = propertyType;
      if (bedrooms) params.bedrooms = bedrooms;
      if (listingType) params.listing_type = listingType;
      if (priceMin) params.price_min = priceMin;
      if (priceMax) params.price_max = priceMax;

      const response = await propertyService.getProperties(params);
      // DRF list views usually paginate and return { results: [...] } or direct array
      const data = response.data.results || response.data;
      setProperties(data);
    } catch (error) {
      console.error("Failed to fetch properties:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProperties();
  }, [searchParams]);

  // Apply filters by writing to URL Search Params
  const handleApplyFilters = (e) => {
    if (e) e.preventDefault();
    const newParams = {};
    if (search) newParams.search = search;
    if (city) newParams.city = city;
    if (propertyType) newParams.property_type = propertyType;
    if (bedrooms) newParams.bedrooms = bedrooms;
    if (listingType) newParams.listing_type = listingType;
    if (priceMin) newParams.price_min = priceMin;
    if (priceMax) newParams.price_max = priceMax;

    setSearchParams(newParams);
    setShowMobileFilters(false);
  };

  // Reset all filters
  const handleResetFilters = () => {
    setSearch('');
    setCity('');
    setPropertyType('');
    setBedrooms('');
    setListingType('');
    setPriceMin('');
    setPriceMax('');
    setSearchParams({});
    setShowMobileFilters(false);
  };

  // Indian currency formatter (Lakhs / Crores)
  const formatPrice = (price, listType) => {
    const num = Number(price);
    if (isNaN(num)) return price;

    let formatted = '';
    if (num >= 10000000) {
      formatted = `₹${(num / 10000000).toFixed(2)} Cr`;
    } else if (num >= 100000) {
      formatted = `₹${(num / 100000).toFixed(2)} Lakh`;
    } else {
      formatted = `₹${num.toLocaleString('en-IN')}`;
    }

    if (listType === 'rent') {
      return `${formatted} / mo`;
    }
    return formatted;
  };

  return (
    <div className="properties-page container animate-fade-in">
      <header className="properties-header">
        <div className="header-info">
          <span className="badge glass">🌟 Verified Listings</span>
          <h1 className="title">Explore Premium <span className="gradient-text">Indian Residences</span></h1>
          <p className="subtitle">Discover verified 2BHKs, 3BHKs, luxury villas, and studio apartments across major cities.</p>
        </div>
        <div className="header-actions">
          <button 
            className="btn btn-outline mobile-filter-btn" 
            onClick={() => setShowMobileFilters(!showMobileFilters)}
          >
            <SlidersHorizontal size={18} /> Filters
          </button>
          <button className="btn btn-outline reset-btn" onClick={handleResetFilters}>
            <RefreshCw size={18} /> Reset
          </button>
        </div>
      </header>

      <div className="properties-layout">
        {/* Sidebar Filters */}
        <aside className={`filters-sidebar glass-card ${showMobileFilters ? 'active' : ''}`}>
          <div className="filters-header">
            <h3>Filter Properties</h3>
            <button className="close-filters-btn" onClick={() => setShowMobileFilters(false)}>×</button>
          </div>
          <form onSubmit={handleApplyFilters} className="filters-form">
            <div className="input-group">
              <label>Search keywords</label>
              <div className="input-wrapper">
                <Search size={16} className="input-icon" />
                <input 
                  type="text" 
                  value={search} 
                  onChange={(e) => setSearch(e.target.value)} 
                  placeholder="e.g., Worli, beachfront, view..." 
                  className="input"
                />
              </div>
            </div>

            <div className="input-group">
              <label>City</label>
              <select value={city} onChange={(e) => setCity(e.target.value)} className="input">
                <option value="">All Cities</option>
                <option value="Mumbai">Mumbai</option>
                <option value="Bangalore">Bangalore</option>
                <option value="Delhi">Delhi</option>
                <option value="Pune">Pune</option>
                <option value="Chennai">Chennai</option>
              </select>
            </div>

            <div className="input-group">
              <label>Listing Type</label>
              <div className="radio-group">
                <button 
                  type="button" 
                  className={`radio-btn ${listingType === '' ? 'active' : ''}`}
                  onClick={() => setListingType('')}
                >
                  All
                </button>
                <button 
                  type="button" 
                  className={`radio-btn ${listingType === 'sale' ? 'active' : ''}`}
                  onClick={() => setListingType('sale')}
                >
                  Buy
                </button>
                <button 
                  type="button" 
                  className={`radio-btn ${listingType === 'rent' ? 'active' : ''}`}
                  onClick={() => setListingType('rent')}
                >
                  Rent
                </button>
              </div>
            </div>

            <div className="input-group">
              <label>Property Type</label>
              <select value={propertyType} onChange={(e) => setPropertyType(e.target.value)} className="input">
                <option value="">All Types</option>
                <option value="apartment">Apartment</option>
                <option value="house">House / Villa</option>
                <option value="condo">Condo</option>
              </select>
            </div>

            <div className="input-group">
              <label>BHK Layout (Bedrooms)</label>
              <select value={bedrooms} onChange={(e) => setBedrooms(e.target.value)} className="input">
                <option value="">Any BHK</option>
                <option value="1">1 BHK / Studio</option>
                <option value="2">2 BHK</option>
                <option value="3">3 BHK</option>
                <option value="4">4 BHK+</option>
              </select>
            </div>

            <div className="input-group">
              <label>Price Range (INR)</label>
              <div className="price-inputs">
                <input 
                  type="number" 
                  value={priceMin} 
                  onChange={(e) => setPriceMin(e.target.value)} 
                  placeholder="Min Price" 
                  className="input price-input"
                />
                <span>-</span>
                <input 
                  type="number" 
                  value={priceMax} 
                  onChange={(e) => setPriceMax(e.target.value)} 
                  placeholder="Max Price" 
                  className="input price-input"
                />
              </div>
            </div>

            <button type="submit" className="btn btn-primary apply-filters-btn">
              Apply Filters
            </button>
          </form>
        </aside>

        {/* Properties Grid */}
        <main className="properties-main">
          {loading ? (
            <div className="loading-grid">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="skeleton-card glass-card">
                  <div className="skeleton-image"></div>
                  <div className="skeleton-content">
                    <div className="skeleton-line title"></div>
                    <div className="skeleton-line text"></div>
                    <div className="skeleton-line details"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : properties.length > 0 ? (
            <div className="property-grid">
              {properties.map(property => (
                <div key={property.id} className="property-card glass-card">
                  <div className="property-image-container">
                    {property.primary_image ? (
                      <img src={property.primary_image} alt={property.title} className="property-image" />
                    ) : (
                      <div className="property-image-placeholder">No Image Available</div>
                    )}
                    <div className="property-badges">
                      <span className="badge-listing-type">
                        {property.listing_type === 'sale' ? 'For Sale' : 'For Rent'}
                      </span>
                      {property.is_featured && <span className="badge-featured">Featured</span>}
                    </div>
                  </div>

                  <div className="property-info">
                    <div className="property-price-tag">
                      {formatPrice(property.price, property.listing_type)}
                    </div>
                    <h3 className="property-title-text">{property.title}</h3>
                    <p className="property-address">
                      <MapPin size={14} className="pin-icon" /> {property.address}, {property.city}
                    </p>

                    <div className="property-amenities">
                      <div className="amenity-item">
                        <Bed size={16} /> <span>{property.bedrooms} BHK</span>
                      </div>
                      <div className="amenity-item">
                        <Bath size={16} /> <span>{property.bathrooms} Baths</span>
                      </div>
                      <div className="amenity-item">
                        <Maximize size={16} /> <span>{Math.round(property.area_sqft)} sqft</span>
                      </div>
                    </div>
                    
                    <div className="card-divider"></div>
                    
                    <div className="property-agent-footer">
                      <div className="agent-avatar-placeholder">
                        {property.agent_name ? property.agent_name.charAt(0) : 'A'}
                      </div>
                      <div className="agent-meta">
                        <span className="agent-label">Listed By</span>
                        <span className="agent-name-text">{property.agent_name || 'Verified Agent'}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-results-card glass-card">
              <h3>No matching properties found</h3>
              <p>Try resetting the filters or modifying your search criteria to discover luxury spaces.</p>
              <button className="btn btn-primary" onClick={handleResetFilters}>Clear All Filters</button>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Properties;
